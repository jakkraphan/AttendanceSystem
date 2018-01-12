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
            }
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
            const obj = {};
            if (this.form.type === 1) {
                obj['table'] = 'employee';
            } else if (this.form.type === 2) {
                obj['table'] = 'supervisor';
            } else if (this.form.type === 3) {
                obj['table'] = 'personnel_manager';
            } else if (this.form.type === 4) {
                obj['table'] = 'system_manager';
            }

            const args = {};
            args.used_id = this.form.userId;
            args.password = this.form.password;
            obj.args = args;
                Cookies.set('user', this.form.userId);
                Cookies.set('mode', this.form.type);
                this.$store.commit('set_user_id', this.form.userId);
                this.$store.commit('set_name', '比利·海灵顿');
                this.$store.commit('set_password', this.form.password);
                this.$store.commit('set_type', this.form.type);
                this.$store.commit('set_information', 'Ass we can');
                this.$store.commit('set_department', 1);
                this.$store.commit('updateMenulist');
                this.$router.push({
                    name: 'home_index'
                });
        }
    }
};
</script>

<style>

</style>
