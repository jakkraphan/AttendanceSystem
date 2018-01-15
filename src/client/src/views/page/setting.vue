<template>
     <div>
        <Card>
            <p slot="title">
                <span v-if="showSwitch"><Icon type="ionic"></Icon> 系统设置 </span>
                <span v-else><Icon type="person"></Icon> 个人设置 </span>         
                <span v-if="type >= 4">
                    <i-switch v-model="showSwitch" size="small"  style="margin: 0 10px 0 10px"></i-switch> 切换
                </span>
            </p>
            <div v-if="showSwitch">
                <Form
                    :label-width="100"
                    label-positon="right">
                    <FormItem label="选择日期：">
                        <Date-picker type="date" v-model="c_date" placeholder="选择日期" style="width: 200px"></Date-picker>
                    </FormItem>
                    <FormItem label="签到时间：">
                        <Time-picker type="time" v-model="begintime" placeholder="选择时间" style="width: 200px"></Time-picker>
                    </FormItem>
                    <FormItem label="签退时间：">
                        <Time-picker type="time" v-model="endtime" placeholder="选择时间" style="width: 200px"></Time-picker>
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
    import Util from '../../libs/util';
    
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
                c_date: '',
                begintime: '',
                endtime: '',
                isUpdateTime: false,
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
                const obj = {
                    'table': 'check_time',
                    'args': {
                        'check_in_time': Util.formatTime(this.begintime),
                        'check_out_time': Util.formatTime(this.endtime)
                    }
                };
                if (this.isUpdateTime) {
                    obj['log'] = 'modify_time';
                    obj['key'] = { 'c_date': Util.formatDate(this.c_date) };
                    this.updateCheckDate(obj);
                } else {
                    obj['log'] = 'add_time';
                    obj['args']['c_date'] = Util.formatDate(this.c_date);
                    this.insertCheckDate(obj);
                }
            },
            cancelTime () {
                this.c_date = '';
                this.begintime = '';
                this.endtime = '';
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
            },
            fetchCheckDate (data) {
                const that = this;
                this.$socket.emit('check_search', data, function (data) {
                    if (data !== undefined && data.length >= 1) {
                        that.isUpdateTime = true;
                        that.begintime = data[0][1];
                        that.endtime = data[0][2];
                    } else {
                        that.isUpdateTime = false;
                        that.begintime = '';
                        that.endtime = '';
                    }
                });
            },
            updateCheckDate (data) {
                this.modifyCheckDate(data, 'update');
            },
            insertCheckDate (data) {
                this.modifyCheckDate(data, 'insert');
            },
            modifyCheckDate (data, methodName) {
                const that = this;
                this.$socket.emit(methodName, data, function (ret) {
                    if (ret) {
                        that.begintime = data['args']['check_in_time'];
                        that.endtime = data['args']['check_out_time'];
                    } else {
                        that.$Message.error('修改失败');
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
        },
        mounted: function () {
            if (this.type >= 4) {
                const today = new Date();
                this.c_date = today;
                today.setDate(today.getDate() + 1);
                this.fetchCheckDate({'c_date': Util.formatDate(today)});
            }
        },
        watch: {
            c_date: function () {
                if (this.c_date !== '') {
                    this.fetchCheckDate({'c_date': Util.formatDate(this.c_date)});
                }
            }
        }
    };
</script>
