<template>
    <Row class="vm-table vm-panel">
        <div class="panel-heading"> 员工管理 </div>
        <div class="panel-body">
            <Row type="flex" justify="space-between" class="control">
                <div class="table-style" >
                    <h3 v-if="this.type >= 3">人事/部门</h3>
                    <i-switch v-model="showSwitch"  v-if="this.type >= 3" style="margin: 0 30px 0 10px"></i-switch>
                    <Select v-model="search_department" clearable style="width:100px;" placeholder="部门">
                        <Option v-for="(value, key) of this.departments" :value="key" :key="key">{{ value }}</Option>
                    </Select>
                    <Input v-model="search_id" placeholder="工号" style="width:100px;margin: 0 10px 0 20px;" v-if="!showSwitch"></Input>
                    <Input v-model="search_name" placeholder="姓名" style="width:100px;margin: 0 10px;" v-if="!showSwitch"></Input>
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
            v-model="userEdit"
            title="编辑员工"
            ok-text="OK"
            cancel-text="Cancel"
            @on-ok="editOk">
            <Form :label-width="80">
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
            v-model="userAdd"
            title="添加员工"
            ok-text="OK"
            cancel-text="Cancel"
            @on-ok="editOk">
            <Form :label-width="80">
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
            v-model="departmentEdit"
            title="编辑部门"
            ok-text="OK"
            cancel-text="Cancel"
            @on-ok="editOk">
            <Form :label-width="80">
                <Form-item label="部门名称">
                    <Input v-model="dataEdit['department_name']"></Input>
                </Form-item>
                <Form-item label="部门详情">
                    <Input v-model="dataEdit['department_detail']" type="textarea"></Input>
                </Form-item>
            </Form>
        </Modal>

        <Modal
            v-model="departmentAdd"
            title="添加部门"
            ok-text="OK"
            cancel-text="Cancel"
            @on-ok="editOk">
            <Form :label-width="80">
                <Form-item label="部门名称">
                    <Input v-model="departmentDataAdd['department_name']"></Input>
                </Form-item>
                <Form-item label="部门详情">
                    <Input v-model="departmentDataAdd['department_detail']" type="textarea"></Input>
                </Form-item>
            </Form>
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
            userEdit: false,
            departmentEdit: false,
            userAdd: false,
            departmentAdd: false,
            modalDelete: false,
            dataEdit: {},
            userDataEdit: {},
            departmentDataEdit: {},
            dataDelete: [],
            userDataAdd: {},
            departmentDataAdd: {},
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
                        let text = this.departments.get(params.row.department);
                        return h(text);
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
                    key: 'department_detail'
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
                this.departmentEdit = true;
            } else {
                this.userEdit = true;
            }
        },
        add: function () {
            if (this.showSwitch) {
                this.departmentAdd = true;
            } else {
                this.userAdd = true;
            }
        },
        editOk: function (data) {
            let keys = [];
            const key = {};
            const args = {};
            const obj = {
                key: key,
                args: args
            };
            if (this.showSwitch) {
                obj['table'] = 'department';
                key['department_number'] = data['department_number'];
                keys = ['department_name', 'department_detail'];
            } else {
                obj['table'] = 'user';
                key['user_id'] = data['user_id'];
                keys = ['name', 'password', 'information', 'department'];
            }
            for (let i in keys) {
                args[i] = this.dataEdit[i];
            }
            this.$socket.emit('', obj, function (status) {
                if (status) {
                    let need2change;
                    let pkey;
                    if (this.showSwitch) {
                        need2change = this.departmentData;
                        pkey = 'department_number';
                    } else {
                        need2change = this.userData;
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
                    this.$Message.error('编辑失败');
                }
            });
        },
        addOk: function (data) {
            let keys;
            let data2add;
            const args = {};
            const obj = {
                args: args
            };
            if (this.showSwitch) {
                obj['table'] = 'department';
                keys = ['department_name', 'department_detail'];
                data2add = this.departmentDataAdd;
            } else {
                obj['table'] = 'user';
                keys = ['name', 'password', 'information', 'department'];
                data2add = this.userDataAdd;
            }
            for (let i in keys) {
                args[i] = data2add[i];
            }
            this.$socket.emit('', obj, function (ret) {
                if (ret) {
                    if (this.showSwitch) {
                        this.userData.unshift(args);
                    } else {
                        this.departmentData.unshift(args);
                    }
                } else {
                    this.$Message.error('插入失败');
                }
            });
        },
        deleteOk: function (data) {
            const obj = {};
            let pkey;
            if (this.showSwitch) {
                obj['table'] = 'department';
                pkey = 'department_number';
            } else {
                obj['table'] = 'user';
                pkey = 'user_id';
            }
            for (let item in data) {
                const key = {};
                key[pkey] = item[pkey];
                obj['key'] = key;
                this.$socket.emit('', obj, function (status) {
                    if (status) {
                        if (this.showSwitch) {
                            this.departmentData = this.departmentData.filter(i => i['number'] !== item['number']);
                        } else {
                            this.userData = this.userData.filter(i => i['number'] !== item['number']);
                        }
                    } else {
                        this.$Message.error('删除失败');
                    }
                });
            }
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
            let btn = [['error', '编辑'], ['success', '删除']];
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
                        if (this.showSwitch) {
                            this.departmentEdit = true;
                        } else {
                            this.userEdit = true;
                        }
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
        this.$socket.emit('', , function(data) {

        });

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
