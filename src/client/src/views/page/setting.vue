<template>
     <div>
        <Card>
            <p slot="title">
                <span v-if="showSwitch"><Icon type="ionic"></Icon> 系统设置 </span>
                <span v-else><Icon type="person"></Icon> 个人设置 </span>         
                <span v-if="this.type >= 4">
                    <i-switch v-model="showSwitch" size="small"  style="margin: 0 10px 0 10px"></i-switch> 切换
                </span>
            </p>
            <div v-if="showSwitch">
                <Form
                    :label-width="100"
                    label-positon="right">
                    <FormItem label="选择日期：">
                        <Date-picker type="date" v-model="date.date" placeholder="选择日期" style="width: 200px"></Date-picker>
                    </FormItem>
                    <FormItem label="签到时间：">
                        <Time-picker type="time" v-model="date.begintime" placeholder="选择时间" style="width: 200px"></Time-picker>
                    </FormItem>
                    <FormItem label="签退时间：">
                        <Time-picker type="time" v-model="date.endtime" placeholder="选择时间" style="width: 200px"></Time-picker>
                    </FormItem>
                    <FormItem label="确认保存：">
                        <Button type="primary" style="width: 99px;" :loading="save_loading" @click="saveTime">保存</Button>
                        <Button type="ghost" style="width: 99px;" @click="cancelTime">取消</Button>                        
                    </FormItem>
                </Form>
            </div>
            <div v-else>
                <Form 
                    ref="user"
                    :label-width="100" 
                    label-position="right">
                     <FormItem label="工号：">
                        <span>{{ user_id }}</span>
                    </FormItem>
                    <FormItem label="姓名：" prop="name">
                        <div style="display:inline-block;width:300px;">
                            <Input v-model="name"></Input>
                        </div>
                    </FormItem>
                    <FormItem label="个人信息：">
                        <Input v-model="information" type="textarea" :autosize="{minRows: 8,maxRows: 10}"></Input>
                    </FormItem>
                    <FormItem label="工作部门：">
                        <span>{{ this.departments[this.department] }}</span>
                    </FormItem>
                    <FormItem label="登录密码：">
                        <Button type="text" size="small" @click="showEditPassword">修改密码</Button>
                    </FormItem>
                    <div>
                        <Button type="text" style="width: 100px;" @click="cancelEditUserInfo">取消</Button>
                        <Button type="primary" style="width: 100px;" :loading="save_loading" @click="saveEdit">保存</Button>
                    </div>
                </Form>
            </div>
        </Card>

        <Modal v-model="editPasswordModal" :closable='false' :mask-closable=false :width="500">
            <h3 slot="header" style="color:#2D8CF0">修改密码</h3>
            <Form ref="editPasswordForm" :model="editPasswordForm" :label-width="100" label-position="right" :rules="passwordValidate">
                <FormItem label="原密码" prop="oldPass" :error="oldPassError">
                    <Input v-model="editPasswordForm.oldPass" placeholder="请输入现在使用的密码"></Input>
                </FormItem>
                <FormItem label="新密码" prop="newPass">
                    <Input v-model="editPasswordForm.newPass" placeholder="请输入新密码，至少6位字符"></Input>
                </FormItem>
                <FormItem label="确认新密码" prop="rePass">
                    <Input v-model="editPasswordForm.rePass" placeholder="请再次输入新密码"></Input>
                </FormItem>
            </Form>
            <div slot="footer">
                <Button type="text" @click="cancelEditPass">取消</Button>
                <Button type="primary" :loading="savePassLoading" @click="saveEditPass">保存</Button>
            </div>
        </Modal>
    </div>
</template>

<<script>
    import { mapGetters } from 'vuex';
    
    export default {
        name: 'setting',
        data () {
            const valideRePassword = (rule, value, callback) => {
                if (value !== this.editPasswordForm.newPass) {
                    callback(new Error('两次输入密码不一致'));
                } else {
                    callback();
                }
            };
            return {
                showSwitch: false,
                save_loading: false,
                editPasswordModal: false, // 修改密码模态框显示
                savePassLoading: false,
                date: {
                    date: '',
                    begintime: '',
                    endtime: ''
                },
                oldname: this.$store.getters.name,
                oldinfo: this.$store.getters.information,
                name: this.$store.getters.name,
                information: this.$store.getters.information,
                oldPassError: '',
                editPasswordForm: {
                    oldPass: '',
                    newPass: '',
                    rePass: ''
                },
                passwordValidate: {
                    oldPass: [
                        { required: true, message: '请输入原密码', trigger: 'blur' }
                    ],
                    newPass: [
                        { required: true, message: '请输入新密码', trigger: 'blur' },
                        { min: 6, message: '请至少输入6个字符', trigger: 'blur' },
                        { max: 32, message: '最多输入32个字符', trigger: 'blur' }
                    ],
                    rePass: [
                        { required: true, message: '请再次输入新密码', trigger: 'blur' },
                        { validator: valideRePassword, trigger: 'blur' }
                    ]
                }
            };
        },
        methods: {
            formatDate (date) {
                const y = date.getFullYear();
                let m = date.getMonth() + 1;
                m = m < 10 ? '0' + m : m;
                let d = date.getDate();
                d = d < 10 ? ('0' + d) : d;
                return y + '-' + m + '-' + d;
            },
            showEditPassword () {
                this.editPasswordModal = true;
            },
            cancelEditPass () {
                this.editPasswordModal = false;
            },
            saveEditPass () {
                const that = this;
                this.$refs['editPasswordForm'].validate((valid) => {
                    if (valid) {
                        that.savePassLoading = true;
                        that.update({
                            'password': that.editPasswordForm.newPass
                        });
                    }
                });
            },
            saveEdit () {
                this.update({
                    'name': this.name,
                    'info': this.information
                });
            },
            cancelEditUserInfo () {
                this.name = this.oldname;
                this.information = this.oldinfo;
            },
            saveTime () {
            },
            cancelTime () {
                this.date.date = '';
                this.date.begintime = '';
                this.date.endtime = '';
            },
            update (data) {
                const that = this;
                this.$socket.emit('change_info', data, function (status) {
                    if (status) {
                        for (let i in data) {
                            that.$store.commit('set_' + i, data[i]);
                        }
                        that.savePassLoading = false;
                        that.editPasswordModal = false;
                        that.$Message.success('更改成功');
                    } else {
                        that.$Message.error('更改出错');
                    }
                });
            }
        },
        computed: {
            ...mapGetters([
                'user_id',
                'type',
                'department',
                'departments'
            ])
        }
    };
</script>
