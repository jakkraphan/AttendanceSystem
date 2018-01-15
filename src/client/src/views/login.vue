<style lang="less">
    @import './login.less';
</style>

<template>
    <div class="login" @keydown.enter="handleSubmit">
        <div class="login-con">
            <Card :bordered="false">
                <p slot="title">
                    <Icon type="log-in"></Icon>
                    欢迎登录
                </p>
                <div class="form-con">
                    <Form ref="loginForm" :model="form" :rules="rules">
                        <FormItem prop="userId">
                            <Input v-model="form.userId" placeholder="请输入工号">
                                <span slot="prepend">
                                    <Icon :size="16" type="person"></Icon>
                                </span>
                            </Input>
                        </FormItem>
                        <FormItem prop="password">
                            <Input type="password" v-model="form.password" placeholder="请输入密码">
                                <span slot="prepend">
                                    <Icon :size="14" type="locked"></Icon>
                                </span>
                            </Input>
                        </FormItem>
                        <FormItem>
                            <RadioGroup v-model="form.type" label="用户类型">
                                <Row>
                                    <Col span="12"><Radio label="1">普通员工</Radio></Col>
                                    <Col span="12"><Radio label="2">部门主管</Radio></Col>
                                </Row>
                                <Row>
                                    <Col span="12"><Radio label="3">人事管理员</Radio></Col>
                                    <Col span="12"><Radio label="4">系统管理员</Radio></Col>
                                </Row>                
                            </RadioGroup>
                        </FormItem>
                        <FormItem>
                            <Button @click="handleSubmit" type="primary" long>登录</Button>
                        </FormItem>
                    </Form>
                </div>
            </Card>
        </div>
    </div>
</template>

<script>
import Cookies from 'js-cookie';
export default {
    data () {
        return {
            form: {
                userId: '',
                password: '',
                type: 1
            },
            rules: {
                userId: [
                    { required: true, message: '账号不能为空', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '密码不能为空', trigger: 'blur' }
                ]
            },
            logins: ['e_login', 'm_login', 'p_login', 's_login']
        };
    },
    methods: {
        handleSubmit () {
            this.$refs.loginForm.validate((valid) => {
                if (valid) {
                    this.login();
                }
            });
        },
        login () {
            const that = this;
            const methodName = this.logins[this.form.type - 1];
            const args = {};

            args.user_id = this.form.userId;
            args.password = this.form.password;
            this.$socket.emit(methodName, args, function (status) {
                if (status !== undefined) {
                    Cookies.set('user', that.form.userId);
                    Cookies.set('mode', that.form.type);
                    that.$store.commit('updateMenulist');
                    that.$store.commit('set_all', status);
                    that.$store.commit('set_type', that.form.type);
                    that.fetchDepartments();
                    that.$router.push({
                        name: 'home_index'
                    });
                } else {
                    that.$Message.error('登录失败');
                }
            });
        },
        fetchDepartments () {
            const that = this;
            const args = {
                'd_id': -1,
                'd_name': -1,
                'order': [['d_id'], ['ASC']]
            };

            this.$socket.emit('d_search', args, function (...args) {
                if (args !== undefined) {
                    that.$store.commit('set_departments', args);
                } else {
                    that.$Message.error('部门信息获取失败');
                }
            });
        }
    }
};
</script>

<style>

</style>
