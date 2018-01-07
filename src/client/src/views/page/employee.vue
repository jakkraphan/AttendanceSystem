<template>
    <VmTable title="人事管理" 
           type="edit" 
           :columns="userColumns" 
           :data="userData"
           :btn="btn"
           v-on:add-ok="add"
           v-on:edit-ok="edit"
           v-on:delete-ok="deletefn"
           class="vm-margin">
  </VmTable>
</template>

<script>
import VmTable from '@/views/main-components/vm-table';
export default {
    name: 'log',
    components: {
        VmTable
    },
    methods: {
        add: function (data) {
            this.dataTable.unshift(data);
        },
        edit: function (data) {
            this.dataTable.forEach(function (elem) {
                if (elem.id === data.id) {
                    for (let i in data) {
                        elem[i] = data[i];
                    }
                }
            });
        },
        deletefn: function (data) {
            for (let i = 0; i < this.dataTable.length; i++) {
                for (let j = 0; j < data.length; j++) {
                    if (this.dataTable[i].id === data[j].id) {
                        this.dataTable.splice(i, 1);
                    }
                }
            }
        }
    },
    data () {
        return {
            userColumns: [
                {
                    title: '工号',
                    key: 'user_id'
                },
                {
                    title: '姓名',
                    key: 'username'
                },
                {
                    title: '密码',
                    key: 'password'
                },
                {
                    title: '个人信息',
                    key: 'information',
                },
                {
                    title: '部门',
                    key: 'department'
                }
            ],
            userData: [
                {
                    user_id: '65416s843154',
                    username: '比利海灵顿',
                    password: '66666666',
                    information: 'ass we can',
                    department: '哲学部'
                },
                {
                    user_id: '6d416sd4c54',
                    username: 'Van',
                    password: '66666666',
                    information: 'fuck♂you',
                    department: '哲学部'
                },
                {
                    user_id: '6d416sd4cdfd',
                    username: '木吉',
                    password: '66666666',
                    information: '吼吼吼吼全给党',
                    department: '哲学部'
                },
                {
                    user_id: '6d416sd4cc4',
                    username: '香蕉君',
                    password: '66662222',
                    information: '蕉迟但到',
                    department: '摔跤部'
                },
                {
                    user_id: '65416s843154',
                    username: '比利海灵顿',
                    password: '66666666',
                    information: 'ass we can',
                    department: '哲学部'
                },
                {
                    user_id: '6d416sd4c54',
                    username: 'Van',
                    password: '66666666',
                    information: 'fuck♂you',
                    department: '哲学部'
                },
                {
                    user_id: '6d416sd4cdfd',
                    username: '木吉',
                    password: '66666666',
                    information: '吼吼吼吼全给党',
                    department: '哲学部'
                },
                {
                    user_id: '6d416sd4cc4',
                    username: '香蕉君',
                    password: '66662222',
                    information: '蕉迟但到',
                    department: '摔跤部'
                },
                {
                    user_id: '65416s843154',
                    username: '比利海灵顿',
                    password: '66666666',
                    information: 'ass we can',
                    department: '哲学部'
                },
                {
                    user_id: '6d416sd4c54',
                    username: 'Van',
                    password: '66666666',
                    information: 'fuck♂you',
                    department: '哲学部'
                },
                {
                    user_id: '6d416sd4cdfd',
                    username: '木吉',
                    password: '66666666',
                    information: '吼吼吼吼全给党',
                    department: '哲学部'
                },
                {
                    user_id: '6d416sd4cc4',
                    username: '香蕉君',
                    password: '66662222',
                    information: '蕉迟但到',
                    department: '摔跤部'
                }
            ],
            btn: [
                ['info', '编辑'],
                ['error', '删除']
            ]
        };
    }
};
</script>

<style lang="less">
    @import '../../theme/index.less';
</style>