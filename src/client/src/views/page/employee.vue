<template>
    <Row class="vm-table vm-panel">
        <div class="panel-heading"> 员工管理 </div>
        <div class="panel-body">
            <Row type="flex" justify="space-between" class="control">
                <div class="table-style" >
                    <h3 v-if="this.type >= 3">人事/部门</h3>
                    <i-switch v-model="showSwitch"  v-if="this.type >= 3" style="margin: 0 30px 0 10px"></i-switch>
                    <Select v-model="search_department" clearable style="width:125px;" placeholder="部门">
                        <Option v-for="(value, key) of this.departments" :value="key" :key="key">{{ value }}</Option>
                    </Select>
                    <Input v-model="search_id" placeholder="工号" style="width:125px;margin: 0 10px 0 20px;" v-if="!showSwitch"></Input>
                    <Input v-model="search_name" placeholder="姓名" style="width:125px;margin: 0 10px;" v-if="!showSwitch"></Input>
                    <Button type="ghost" style="margin: 0 10px 0 10px" @click="deepSearch">Deep Dark Search</Button>
                </div>
                <div class="search-bar">
                    <Input placeholder="Please enter ..." v-model="keyword" style="width: 200px"></Input>
                    <Button type="ghost" @click="search" icon="search"></Button>
                </div>
            </Row>
            <div class="edit" v-if="this.type >= 3">
                <Button @click="add" icon="plus-round">添加</Button>
                <Button  :disabled="deleteDisabled" @click="modalDelete = true" icon="trash-a">删除</Button>
            </div>
            <Table :columns="departmentsColumns" :data="showDepartmentData" v-if="showSwitch"></Table>
            <Table :columns="showColumns" :data="showData" @on-selection-change="selectChange" v-else></Table>
            <Row type="flex" justify="space-between" class="footer" v-if="showSwitch">
                <div class="info-bar">
                    Show<Input-number class="input-number" v-model="showNum" :max="departmentData.length" :min="1" @on-change="updataShowData ">{{ showNum }}</Input-number>/ Page
                </div>
                <div class="page">
                <span class="total">Total {{ departmentData.length }}</span>
                <Page :total="departmentData.length" :current="currentPage" :page-size="showNum" @on-change="pageChange"></Page>
                </div>
            </Row>
            <Row type="flex" justify="space-between" class="footer" v-else>
                <div class="info-bar">
                    Show<Input-number class="input-number" v-model="showNum" :max="userData.length" :min="1" @on-change="updataShowData ">{{ showNum }}</Input-number>/ Page
                </div>
                <div class="page">
                <span class="total">Total {{ userData.length }}</span>
                <Page :total="userData.length" :current="currentPage" :page-size="showNum" @on-change="pageChange"></Page>
                </div>
            </Row>
        </div>
        
        <Modal
            v-model="userModalEdit"
            title="编辑员工"
            ok-text="OK"
            cancel-text="Cancel"
            @on-ok="editOk">
            <Form :label-width="80" ref="dataEdit" :model="dataEdit">
                <Form-item label="姓名">
                    <Input v-model="dataEdit['name']"></Input>
                </Form-item>
                <Form-item label="密码">
                    <Input v-model="dataEdit['password']"></Input>
                </Form-item>
                <Form-item label="个人信息">
                    <Input v-model="dataEdit['information']"></Input>
                </Form-item>
                <Form-item label="部门">
                    <Select v-model="dataEdit['department']">
                        <Option v-for="(value, key) of this.departments" :value="key" :key="key">{{ value }}</Option>
                    </Select>
                </Form-item>
            </Form>
        </Modal>

        <Modal
            v-model="userModalAdd"
            title="添加员工"
            ok-text="OK"
            cancel-text="Cancel"
            @on-ok="addOk">
            <Form :label-width="80" ref="userDataAdd" :model="userDataAdd">
                <Form-item label="姓名">
                    <Input v-model="userDataAdd['name']"></Input>
                </Form-item>
                <Form-item label="密码">
                    <Input v-model="userDataAdd['password']"></Input>
                </Form-item>
                <Form-item label="个人信息">
                    <Input v-model="userDataAdd['information']"></Input>
                </Form-item>
                <Form-item label="部门">
                    <Select v-model="userDataAdd['department']">
                        <Option v-for="(value, key) of this.departments" :value="key" :key="key">{{ value }}</Option>
                    </Select>
                </Form-item>
            </Form>
        </Modal>

        <Modal
            v-model="departmentModalEdit"
            title="编辑部门"
            ok-text="OK"
            cancel-text="Cancel"
            @on-ok="editOk">
            <Form :label-width="80" ref="dataEdit" :model="dataEdit">
                <Form-item label="部门名称">
                    <Input v-model="dataEdit['department_name']"></Input>
                </Form-item>
                <Form-item label="部门详情">
                    <Input v-model="dataEdit['department_info']" type="textarea"></Input>
                </Form-item>
            </Form>
        </Modal>

        <Modal
            v-model="departmentModalAdd"
            title="添加部门"
            ok-text="OK"
            cancel-text="Cancel"
            @on-ok="addOk">
            <Form :label-width="80" ref="depertmentDataAdd" :model="departmentDataAdd">
                <Form-item label="部门名称">
                    <Input v-model="departmentDataAdd['department_name']"></Input>
                </Form-item>
                <Form-item label="部门详情">
                    <Input v-model="departmentDataAdd['department_info']" type="textarea"></Input>
                </Form-item>
            </Form>
        </Modal>

        <Modal
            v-model="modalDelete"
            title="Delete"
            ok-text="OK"
            cancel-text="Cancel"
            @on-ok="deleteOk">
            Are you sure to delete this data?
        </Modal>
        
    </Row>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    name: 'employee',
    data () {
        return {
            deleteDisabled: true,
            search_department: '',
            search_id: '',
            search_name: '',
            showData: [],
            showDepartmentData: [],
            showNum: 10,
            showSwitch: false,
            currentPage: 1,
            keyword: '',
            userModalEdit: false,
            departmentModalEdit: false,
            userModalAdd: false,
            departmentModalAdd: false,
            modalDelete: false,
            dataEdit: {},
            userDataEdit: {},
            departmentDataEdit: {},
            dataDelete: [],
            userDataAdd: {
                'edit_name': '',
                'password': '',
                'information': '',
                'department': ''
            },
            departmentDataAdd: {

            },
            userData: [],
            userColumns: [
                {
                    title: '工号',
                    key: 'user_id',
                    sortable: true
                },
                {
                    title: '姓名',
                    key: 'name',
                    sortable: true
                },
                {
                    title: '密码',
                    key: 'password'
                },
                {
                    title: '个人信息',
                    key: 'information'
                },
                {
                    title: '部门',
                    key: 'department',
                    sortable: true,
                    render: (h, params) => {
                        let text = this.departments[params.row.department];
                        return h('Tag', text);
                    }
                }
            ],
            departmentData: [],
            departmentsColumns: [
                {
                    type: 'selection',
                    width: 60,
                    align: 'center'
                },
                {
                    title: '部门编号',
                    key: 'department_number',
                    sortable: true
                },
                {
                    title: '部门名称',
                    key: 'department_name',
                    sortable: true
                },
                {
                    title: '部门信息',
                    key: 'department_info'
                },
                {
                    title: '操作',
                    key: 'action',
                    width: 150,
                    align: 'center',
                    render: this.renderOperate
                }
            ]
        };
    },
    methods: {
        edit: function () {
            if (this.showSwitch) {
                this.departmentModalEdit = true;
            } else {
                this.userModalEdit = true;
            }
        },
        add: function () {
            if (this.showSwitch) {
                this.departmentModalAdd = true;
            } else {
                this.userModalAdd = true;
            }
        },
        editOk: function () {
            const that = this;
            let data = this.dataEdit;
            const key = {};
            const args = {};
            const obj = {
                key: key,
                args: args
            };
            if (this.showSwitch) {
                obj['table'] = 'department';
                obj['log'] = 'modify_department';
                key['d_id'] = data['department_number'];
                args['d_name'] = data['department_name'];
                args['d_info'] = data['department_info'];
            } else {
                obj['table'] = 'user';
                obj['log'] = 'modify_user';
                key['user_id'] = data['user_id'];
                args['name'] = data['name'];
                args['password'] = data['password'];
                args['info'] = data['information'];
                args['d_id'] = data['department'];
            }
            this.$socket.emit('update', obj, function (status) {
                if (status) {
                    let need2change;
                    let pkey;
                    if (that.showSwitch) {
                        need2change = that.departmentData;
                        pkey = 'department_number';
                    } else {
                        need2change = that.userData;
                        pkey = 'user_id';
                    }
                    need2change.forEach(elem => {
                        if (elem[pkey] === data[pkey]) {
                            for (let i in data) {
                                elem[i] = data[i];
                            }
                        }
                    });
                } else {
                    that.$Message.error('编辑失败');
                }
            });
        },
        addOk: function (data) {
            const that = this;
            const args = {};
            const obj = {
                args: args
            };
            if (this.showSwitch) {
                obj['table'] = 'department';
                args['d_name'] = this.departmentDataAdd['department_name'];
                args['d_info'] = this.departmentDataAdd['department_info'];
            } else {
                obj['table'] = 'user';
                obj['log'] = 'add_user';
                args['name'] = this.userDataAdd['name'];
                args['password'] = this.userDataAdd['password'];
                args['info'] = this.userDataAdd['information'];
                args['d_id'] = this.userDataAdd['department'];
            }
            this.$socket.emit('insert', obj, function (ret) {
                if (ret) {
                    if (that.showSwitch) {
                        that.userData.unshift(args);
                    } else {
                        that.departmentData.unshift(args);
                    }
                } else {
                    that.$Message.error('插入失败');
                }
            });
        },
        deleteOk: function () {
            const that = this;
            const obj = {};
            let pkey;
            if (this.showSwitch) {
                obj['table'] = 'department';
                obj['log'] = 'del_department';
                pkey = ['department_number', 'd_id'];
            } else {
                obj['table'] = 'user';
                obj['log'] = 'del_user';
                pkey = ['user_id', 'user_id'];
            }
            for (let item of this.dataDelete) {
                const key = {};
                key[pkey[0]] = item[pkey[0]];
                obj['args'] = key;
                this.$socket.emit('delete', obj, function (status) {
                    if (status) {
                        if (that.showSwitch) {
                            that.departmentData = that.departmentData.filter(i => i['number'] !== item['number']);
                        } else {
                            that.userData = that.userData.filter(i => i['number'] !== item['number']);
                        }
                    } else {
                        that.$Message.error('删除失败');
                    }
                });
            }
            this.dataDelete = [];
        },
        pageChange: function (page) {
            this.currentPage = page;
            this.updataShowData();
        },
        updataShowData: function () {
            let startPage = (this.currentPage - 1) * this.showNum;
            let endPage = startPage + this.showNum;
            if (!this.showSwitch) {
                this.showData = this.userData.slice(startPage, endPage);
            } else {
                this.showDepartmentData = this.departmentData.slice(startPage, endPage);
            }
        },
        deepSearch: function () {
            let obj = {};
            if (this.search_department !== '') {
                obj['d_id'] = parseInt(this.search_department);
            } else if (this.type >= 3) {
                obj['d_id'] = -1;
            } else {
                obj['d_id'] = this.department;
            }
            if (this.search_name !== '') {
                obj['name'] = this.search_name;
            } else {
                obj['name'] = -1;
            }
            if (this.search_id !== '') {
                obj['user_id'] = parseInt(this.search_id);
            } else {
                obj['user_id'] = -1;
            }
            obj['order'] = [['user_id'], ['ASC']];
            this.fetchUser(obj);
        },
        search: function () {
            let that = this;
            let tempData = that.userData;
            that.showData = [];
            tempData.forEach(function (elem) {
                for (let i in elem) {
                    if (elem[i].toString().indexOf(that.keyword) > -1) {
                        that.showData.push(elem);
                        return;
                    }
                }
            });
        },
        selectChange: function (data) {
            this.dataDelete = data;
        },
        remove: function (index) {
            this.showData.splice(index, 1);
        },
        renderOperate: function (h, params) {
            let btn = [['success', '编辑'], ['error', '删除']];
            const btn1 = h('Button', {
                props: {
                    type: btn[0][0],
                    size: 'small'
                },
                style: {
                    marginRight: '5px'
                },
                on: {
                    click: () => {
                        for (let i in params.row) {
                            if (i !== '_index' && i !== '_rowKey') {
                                this.dataEdit[i] = params.row[i];
                            }
                        }
                        this.edit();
                    }
                }
            }, btn[0][1]);

            const btn2 = h('Button', {
                props: {
                    type: btn[1][0],
                    size: 'small'
                },
                style: {
                    marginRight: '5px'
                },
                on: {
                    click: () => {
                        this.dataDelete.push(params.row);
                        this.modalDelete = true;
                    }
                }
            }, btn[1][1]);

            return h('div', [btn1, btn2]);
        },
        convertKey: function (value) {
            let returnValue = value;
            this.columns.forEach(function (elem) {
                for (let i in elem) {
                    if (i === 'key' && elem[i] === value) {
                        returnValue = elem.title;
                    }
                }
            });
            return returnValue;
        },
        fetchUser: function (obj) {
            const that = this;
            this.$socket.emit('e_search', obj, function (...args) {
                if (args !== undefined) {
                    that.userData = [];
                    for (let i of args) {
                        that.userData.push({
                            'user_id': i[0],
                            'department': i[1],
                            'password': i[2],
                            'name': i[3],
                            'information': i[4]
                        });
                    }
                } else {
                    that.$Message.error('数据获取失败');
                }
            });
        },
        fetchDepartment: function (obj) {
            const that = this;
            this.$socket.emit('d_search', obj, function (...args) {
                if (args !== undefined) {
                    that.departmentData = [];
                    for (let i of args) {
                        that.departmentData.push({
                            'department_number': i[0],
                            'department_name': i[1],
                            'department_info': i[2]
                        });
                    }
                } else {
                    that.$Message.error('数据获取失败');
                }
            });
        }
    },
    computed: {
        showColumns: function () {
            let showColumn = this.userColumns.slice();
            if (this.type >= 3) {
                showColumn.unshift({
                    type: 'selection',
                    width: 60,
                    align: 'center'
                });
                showColumn.push({
                    title: '操作',
                    key: 'action',
                    width: 150,
                    align: 'center',
                    render: this.renderOperate
                });
            }
            return showColumn;
        },
        ...mapGetters([
            'user_id',
            'type',
            'department',
            'departments'
        ])
    },
    watch: {
        userData: function () {
            this.showData = this.userData.slice(0, this.showNum);
        },
        departmentData: function () {
            this.showDepartmentData = this.departmentData.slice(0, this.showNum);
        },
        dataDelete: function () {
            if (this.dataDelete.length === 0) {
                this.deleteDisabled = true;
            } else {
                this.deleteDisabled = false;
            }
        }
    },
    mounted: function () {
        let obj = {};
        if (this.type >= 3) {
            obj['d_id'] = -1;
        } else {
            obj['d_id'] = this.department;
        }
        obj['name'] = -1;
        obj['user_id'] = -1;
        obj['order'] = [['user_id'], ['ASC']];
        this.fetchUser(obj);
        if (this.type >= 3) {
            obj = {
                'd_id': -1,
                'd_name': -1,
                'order': [['d_id'], ['ASC']]
            };
            this.fetchDepartment(obj);
        }
        this.showData = this.userData.slice(0, this.showNum);
        this.showDepartmentData = this.departmentData.slice(0, this.showNum);
    }
};
</script>

<style scoped>
.table-style{
      display: inline;
      align-items: center;
}
</style>
