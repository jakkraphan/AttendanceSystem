<template>
     <div>
        <Card>
            <p slot="title">
                <Icon type="person"></Icon>
                个人信息
            </p>
            <div>
                <Form 
                    ref="user"
                    :label-width="100" 
                    label-position="right">
                     <FormItem label="工号：">
                        <span>{{ user.user_id }}</span>
                    </FormItem>
                    <FormItem label="姓名：" prop="name">
                        <div style="display:inline-block;width:300px;">
                            <Input v-model="user.name" ></Input>
                        </div>
                    </FormItem>
                    <FormItem label="个人信息：">
                        <Input v-model="user.information" type="textarea" :autosize="{minRows: 8,maxRows: 10}"></Input>
                    </FormItem>
                    <FormItem label="工作部门：">
                        <span>{{ user.department }}</span>
                    </FormItem>
                    <FormItem label="登录密码：">
                        <Button type="text" size="small" @click="showEditPassword">修改密码</Button>
                    </FormItem>
                    <div>
                        <Button type="text" style="width: 100px;" @click="cancelEditUserInfor">取消</Button>
                        <Button type="primary" style="width: 100px;" :loading="save_loading" @click="saveEdit">保存</Button>
                    </div>
                </Form>
            </div>
        </Card>

        <Modal v-model="editPasswordModal" :closable='false' :mask-closable=false :width="500">
            <h3 slot="header" style="color:#2D8CF0">修改密码</h3>
            <Form ref="editPasswordForm" :model="editPasswordForm" :label-width="100" label-position="right" :rules="passwordValidate">
                <FormItem label="原密码" prop="oldPass" :error="oldPassError">
                    <Input v-model="editPasswordForm.oldPass" placeholder="请输入现在使用的密码" ></Input>
                </FormItem>
                <FormItem label="新密码" prop="newPass">
                    <Input v-model="editPasswordForm.newPass" placeholder="请输入新密码，至少6位字符" ></Input>
                </FormItem>
                <FormItem label="确认新密码" prop="rePass">
                    <Input v-model="editPasswordForm.rePass" placeholder="请再次输入新密码" ></Input>
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
                user: {
                    user_id: 233333333,
                    name: '比利',
                    information: 'ass ♂ we ♂ can',
                    department: '哲♂学♂部'
                },
                save_loading: false,
                editPasswordModal: false, // 修改密码模态框显示
                savePassLoading: false,
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
                this.$refs['editPasswordForm'].validate((valid) => {
                    if (valid) {
                        this.savePassLoading = true;
                        // you can write ajax request here
                    }
                });
            }
        }
    };
</script>

<style scoped>
    .own-space-btn-box {
  margin-bottom: 10px;
}
.own-space-btn-box button {
  padding-left: 0;
}
.own-space-btn-box button span {
  color: #2D8CF0;
  transition: all .2s;
}
.own-space-btn-box button span:hover {
  color: #0C25F1;
  transition: all .2s;
}
.own-space-tra {
  width: 10px;
  height: 10px;
  transform: rotate(45deg);
  position: absolute;
  top: 50%;
  margin-top: -6px;
  left: -3px;
  box-shadow: 0 0 2px 3px rgba(0,0,0,0.1);
  background-color: white;
  z-index: 100;
}
.own-space-input-identifycode-con {
  position: absolute;
  width: 200px;
  height: 100px;
  right: -220px;
  top: 50%;
  margin-top: -50px;
  border-radius: 4px;
  box-shadow: 0 0 2px 3px rgba(0,0,0,0.1);
}
</style>
