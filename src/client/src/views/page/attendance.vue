<template>
    <Row class="vm-table vm-panel">
        <div class="panel-heading"> 员工考勤 </div>
        <div class="panel-body">
            <Row type="flex" justify="space-between" class="control">
                <div class="table-style">
                    <h3  v-if="type === 2 || type === '2'">考勤/查看</h3>
                    <i-switch v-model="showSwitch" style="margin: 0 10px 0 5px"  v-if="type === 2 || type === '2'"></i-switch>
                    <Select v-model="search_department" clearable style="width:100px; margin: 0 5px;" placeholder="部门" v-if="this.type >= 2 && showSwitch">
                        <Option v-for="(value, key) of this.departments" :value="key" :key="key">{{ value }}</Option>
                    </Select>
                    <Input v-model="search_id" placeholder="工号" style="width:100px;margin: 0 5px;" v-if="this.type >= 2 && showSwitch"></Input>
                    <Input v-model="search_name" placeholder="姓名" style="width:100px;margin: 0 5px;" v-if="this.type >= 2 && showSwitch"></Input>
                    <DatePicker v-model="begintime" type="date" placeholder="最小日期" style="width: 125px; margin: 0 5px"></DatePicker>
                    <DatePicker v-model="endtime" type="date" placeholder="最大日期"  style="width: 125px; margin: 0 5px"></DatePicker>
                    <Select v-model="search_group" style="width:100px; margin: 0 5px;" placeholder="分组">
                        <Option v-for="(value, key) of group" :value="key" :key="key">{{ value }}</Option>
                    </Select>         
                    <Button type="ghost" style="margin: 0 10px 0 10px" @click="deepSearch">Deep Search</Button>
                </div>
                <div class="search-bar">
                    <Input placeholder="Please enter ..." v-model="keyword" style="width: 200px"></Input>
                    <Button type="ghost" @click="search" icon="search"></Button>
                </div>
            </Row>
            <div class="edit" v-if="this.showSwitch">
                <Button @click="add" icon="plus-round" v-if="type >= 4">添加</Button>
                <Button  :disabled="deleteDisabled" @click="modalDelete = true" icon="trash-a" v-if="type >= 4">删除</Button>
                <Tag type="dot" color="blue" style="margin: 0 5px 0 20px;">查询顺序</Tag>
                <Checkbox-group v-model="korder" style="display: inline;">
                    <Checkbox label="attendance_table.user_id">
                        <span>员工工号</span>
                    </Checkbox>
                    <Checkbox label="d_id">
                        <span>部门编号</span>
                    </Checkbox>
                    <Checkbox label="status">
                        <span>上班状态</span>
                    </Checkbox>
                </Checkbox-group>
                <template v-for="i in korder.length">
                    <Select v-model="vorder[i-1]" style="width:100px; margin: 0 5px;" :key="i">
                        <Option v-for="item in vorderv" :value="item.value" :key="item">{{ item.label }}</Option>
                    </Select>
                </template>
            </div>
            <div class="edit" v-else>
                <Tag type="dot" color="blue">{{this.date}}</Tag>                
                <Button @click="checkin" style="width: 100px;margin: 0 5px" type="primary" :disabled="today.is_check_in">签到</Button>
                <Button @click="checkout" style="width: 100px;margin: 0 5px" type="primary" :disabled="today.is_check_out">签退</Button>
            </div>
            <Table :columns="selfColumns" :data="showSelfData" v-if="!showSwitch"></Table>
            <Table :columns="showColumns" :data="showAllData" @on-selection-change="selectChange" v-else></Table>
            <Row type="flex" justify="space-between" class="footer" v-if="!showSwitch">
                <div class="info-bar">
                    Show<Input-number class="input-number" v-model="showNum" :max="selfData.length" :min="1" @on-change="updataShowData ">{{ showNum }}</Input-number>/ Page
                </div>
                <div class="page">
                <span class="total">Total {{ selfData.length }}</span>
                <Page :total="selfData.length" :current="currentPage" :page-size="showNum" @on-change="pageChange"></Page>
                </div>
            </Row>
            <Row type="flex" justify="space-between" class="footer" v-else>
                <div class="info-bar">
                    Show<Input-number class="input-number" v-model="showNum" :max="allData.length" :min="1" @on-change="updataShowData ">{{ showNum }}</Input-number>/ Page
                </div>
                <div class="page">
                <span class="total">Total {{ allData.length }}</span>
                <Page :total="allData.length" :current="currentPage" :page-size="showNum" @on-change="pageChange"></Page>
                </div>
            </Row>
        </div>

        <Modal
            v-model="modalEdit"
            title="编辑考勤"
            ok-text="OK"
            cancel-text="Cancel"
            @on-ok="editOk">
            <Form :label-width="80" ref="dataEdit" :model="dataEdit">
                <Form-item label="员工工号">
                    <Input v-model="dataEdit['user_id']"></Input>
                </Form-item>
                <Form-item label="出勤日期">
                    <Date-picker type="date" v-model="dataEdit['date']"></Date-picker>
                </Form-item>
                <Form-item label="签到时间">
                    <Time-picker type="time" v-model="dataEdit['begintime']"></Time-picker>                    
                </Form-item>
                <Form-item label="签退时间">
                    <Time-picker type="time" v-model="dataEdit['endtime']"></Time-picker>                    
                </Form-item>
                 <Form-item label="考勤状态">
                    <Select v-model="dataEdit['status']">
                        <Option v-for="(value, index) in this.status" :value="index" :key="index">{{ value }}</Option>
                    </Select>                   
                </Form-item>
            </Form>
        </Modal>

        <Modal
            v-model="modalAdd"
            title="添加考勤"
            ok-text="OK"
            cancel-text="Cancel"
            @on-ok="editOk">
            <Form :label-width="80" ref="dataAdd" :model="dataAdd">
               <Form-item label="员工工号">
                    <Input v-model="dataAdd['user_id']"></Input>
                </Form-item>
                <Form-item label="出勤日期">
                    <Date-picker type="date" v-model="dataAdd['date']"></Date-picker>
                </Form-item>
                <Form-item label="签到时间">
                    <Time-picker type="time" v-model="dataAdd['begintime']"></Time-picker>                    
                </Form-item>
                <Form-item label="签退时间">
                    <Time-picker type="time" v-model="dataAdd['endtime']"></Time-picker>                    
                </Form-item>
                 <Form-item label="考勤状态">
                    <Select v-model="dataAdd['status']">
                        <Option v-for="(value, index) in this.status" :value="index" :key="index">{{ value }}</Option>
                    </Select>                   
                </Form-item>
            </Form>
        </Modal>

        <Modal v-model="modalDeep"
            title="分类查询"
            width="800">
            <i-table :columns="showModalColumns" :data="modalData"></i-table>            
        </Modal>
    </Row>
</template>

<script>
import { mapGetters } from 'vuex';
import Util from '../../libs/util';

export default {
    name: 'attendance',
    data () {
        return {
            date: Util.formatDate(new Date()),
            begintime: '',
            endtime: '',
            deleteDisabled: true,
            search_department: '',
            search_id: '',
            search_name: '',
            search_group: '',
            selfData: [],
            allData: [],
            showSelfData: [],
            showAllData: [],
            showSwitch: false,
            showNum: 10,
            currentPage: 1,
            keyword: '',
            modalDelete: false,
            dataDelete: [],
            modalEdit: false,
            dataEdit: {},
            modalAdd: false,
            dataAdd: {},
            modalDeep: false,
            today: {
                is_check_in: false,
                is_check_out: false
            },
            modalData: [],
            modalColumns: [{
                title: '状态',
                key: 'status',
                sortable: true
            },
            {
                title: '天数',
                key: 'count',
                sortable: true
            }],
            selfColumns: [
                {
                    title: '工号',
                    key: 'user_id',
                    sortable: true
                },
                {
                    title: '日期',
                    key: 'date',
                    sortable: true
                },
                {
                    title: '签到时间',
                    key: 'begintime',
                    sortable: true
                },
                {
                    title: '签退时间',
                    key: 'endtime',
                    sortable: true
                },
                {
                    title: '状态',
                    key: 'status',
                    sortable: true,
                    render: (h, params) => {
                        let text = this.status[params.row.status];
                        return (text);
                    }
                }
            ],
            status: [
                '未定', '迟到', '早退', '迟到早退', '缺勤', '不正常上班', '正常', '出差', '请假'
            ],
            korder: [],
            vorder: ['ASC', 'ASC', 'ASC'],
            vorderv: [{ value: 'ASC', label: '顺序' }, {value: 'DESC', label: '逆序'}],
            group: {'': '不分组', user: '用户', department: '部门', status: '状态'}
        };
    },
    methods: {
        edit: function () {
            this.modalEdit = true;
        },
        add: function () {
            this.modalAdd = true;
        },
        editOk: function () {
            const that = this;
            const obj = {
                'table': 'attendance_table',
                'log': 'edit_status',
                'key': {
                    'user_id': this.dataEdit['user_id'],
                    'm_date': Util.formatDate(this.dataEdit['date'])
                },
                'args': {
                    'check_in_time': Util.formatTime(this.dataEdit['begintime']),
                    'check_out_time': Util.formatTime(this.dataEdit['endtime']),
                    'status': this.dataEdit['status']
                }
            };
            this.$socket.emit('update', obj, function (status) {
                if (status) {
                    that.fetchAllData();
                } else {
                    that.$Message.error('编辑失败');
                }
            });
        },
        addOk: function () {
            const that = this;
            const obj = {
                'table': 'attendance_table',
                'args': {
                    'user_id': this.dataAdd['user_id'],
                    'm_date': Util.formatDate(this.dataAdd['date']),
                    'check_in_time': this.dataAdd['begintime'],
                    'check_out_time': this.dataAdd['endtime'],
                    'status': this.dataAdd['status']
                }
            };
            this.$socket.emit('insert', obj, function (status) {
                if (status) {
                    that.allData.unshift(this.dataAdd);
                } else {
                    that.$Message.error('插入失败');
                }
            });
        },
        deleteOk: function () {
            const that = this;
            const obj = {
                'table': 'attendance_table',
                'log': 'del_attendance',
                'key': {}
            };
            for (let item in this.dataDelete) {
                const key = {};
                key['user_id'] = item['user_id'];
                key['m_date'] = item['date'];
                obj['key'] = key;
                this.$socket.emit('delete', obj, function (status) {
                    if (status) {
                        that.allData = that.allData.filter(i => i['number'] !== item['number']);
                    } else {
                        that.$Message.error('删除失败');
                    }
                });
            }
        },
        checkin: function () {
            const obj = {
                table: 'attendance_table',
                log: 'checkin',
                key: {
                    'user_id': this.user_id,
                    'm_date': this.date
                },
                args: {
                    'check_in_time': Util.formatTime(new Date())
                }
            };
            this.check_in_out(obj, 'is_check_in');
        },
        checkout: function () {
            if (!this.today.is_check_in) {
                this.$Message.error('请先签到');
                return;
            }
            const obj = {
                table: 'attendance_table',
                log: 'checkout',
                key: {
                    'user_id': this.user_id,
                    'm_date': this.date
                },
                args: {
                    'check_out_time': Util.formatTime(new Date())
                }
            };
            this.check_in_out(obj, 'is_check_out');
        },
        check_in_out: function (data, i) {
            const that = this;
            this.$socket.emit('update', data, function (status) {
                if (status) {
                    that.today[i] = true;
                    that.$Message.success('打卡成功');
                } else {
                    that.$Message.error('打卡失败');
                }
            });
        },
        pageChange: function (page) {
            this.currentPage = page;
            this.updataShowData();
        },
        updataShowData: function () {
            let startPage = (this.currentPage - 1) * this.showNum;
            let endPage = startPage + this.showNum;
            if (!this.showSwitch) {
                this.showSelfData = this.selfData.slice(startPage, endPage);
            } else {
                this.showAllData = this.allData.slice(startPage, endPage);
            }
        },
        deepSearch: function () {
            const obj = {
                'user_id': -1,
                'name': -1,
                'start': -1,
                'end': -1,
                'status': -1,
                'order': [['attendance_table.user_id', 'm_date'], ['ASC', 'DESC']]
            };
            if (this.search_department !== '') {
                obj['d_id'] = parseInt(this.search_department);
            } else if (this.type >= 3) {
                obj['d_id'] = -1;
            } else {
                obj['d_id'] = parseInt(this.department);
            }
            if (this.search_name !== '') {
                obj['name'] = this.search_name;
            }
            if (this.search_id !== '') {
                obj['user_id'] = parseInt(this.search_id);
            } else if (this.type > 1) {
                obj['user_id'] = -1;
            }
            if (this.begintime !== '') {
                obj['start'] = Util.formatDate(this.begintime);
            }
            if (this.endtime !== '') {
                obj['end'] = Util.formatDate(this.endtime);
            }
            if (this.korder.length > 0) {
                const newVorder = this.vorder.slice(0, this.korder.length);
                obj['order'] = [this.korder, newVorder];
            }
            if (this.search_group !== '') {
                this.sum_search(obj);
            } else {
                this.fetchData(obj, !this.showSwitch);
            }
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
                        this.modalEdit = true;
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
        sum_search: function (obj) {
            const that = this;
            obj['group'] = this.search_group;
            this.$socket.emit('sum_a_search', obj, function (...args) {
                if (args !== undefined && args.length > 0) {
                    const array = [];
                    if (that.search_group === 'user') {
                        args.forEach(item => {
                            array.push({
                                'user_id': item[0],
                                'd_id': item[1],
                                'status': item[2],
                                'count': item[3]
                            });
                        });
                    } else if (that.search_group === 'department') {
                        args.forEach(item => {
                            array.push({
                                'd_id': item[0],
                                'status': item[1],
                                'count': item[2]
                            });
                        });
                    } else {
                        args.forEach(item => {
                            array.push({
                                'status': item[0],
                                'count': item[1]
                            });
                        });
                    }
                    that.modalData = array;
                    that.modalDeep = true;
                } else {
                    that.$Message.error('分组查询失败');
                }
            });
        },
        fetchData: function (obj, isSelf) {
            const that = this;
            const flag = isSelf;
            this.$socket.emit('attendance_search', obj, function (...args) {
                if (args !== undefined && args.length > 0) {
                    let data2push = [];
                    for (let i of args[0]) {
                        data2push.push({
                            'user_id': i[0],
                            'date': i[1],
                            'begintime': i[2],
                            'endtime': i[3],
                            'status': i[4]
                        });
                    }
                    if (flag) {
                        that.selfData = data2push;
                    } else {
                        that.allData = data2push;
                    }
                } else {
                    that.$Message.error('失败');
                }
            });
        },
        fetchAllData () {
            const obj = {
                'user_id': -1,
                'd_id': -1,
                'name': -1,
                'start': -1,
                'end': -1,
                'status': -1,
                'order': [['user.user_id', 'm_date'], ['ASC', 'DESC']]
            };
            this.fetchData(obj, false);
        },
        check_status () {
            const today = new Date();
            for (let i of this.selfData) {
                if (Util.checkDate(today, new Date(i['date']))) {
                    if (i['begintime'] !== null) {
                        this.today.is_check_in = true;
                    }
                    if (i['endtime'] !== null) {
                        this.today.is_check_out = true;
                    }
                    return;
                }
            }
        }
    },
    computed: {
        showColumns: function () {
            let showColumn = this.selfColumns.slice();
            if (this.type >= 4) {
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
        showModalColumns: function () {
            let showModalColumn = this.modalColumns.slice();
            if (this.search_group === 'user') {
                showModalColumn.unshift({
                    title: '部门',
                    key: 'd_id',
                    sortable: true,
                    render: (h, params) => {
                        let text = this.departments[params.row.d_id];
                        return (text);
                    }
                });
                showModalColumn.unshift({
                    title: '工号',
                    key: 'user_id',
                    sortable: true
                });
            } else if (this.search_group === 'department') {
                showModalColumn.unshift({
                    title: '部门',
                    key: 'd_id',
                    sortable: true,
                    render: (h, params) => {
                        let text = this.departments[params.row.d_id];
                        return (text);
                    }
                });
            }
            return showModalColumn;
        },
        ...mapGetters([
            'user_id',
            'type',
            'department',
            'departments'
        ])
    },
    watch: {
        selfData: function () {
            this.showSelfData = this.selfData.slice(0, this.showNum);
            this.check_status();
        },
        allData: function () {
            this.showAllData = this.allData.slice(0, this.showNum);
        },
        dataDelete: function () {
            if (this.dataDelete.length === 0) {
                this.deleteDisabled = true;
            } else {
                this.deleteDisabled = false;
            }
        }
    },
    created: function () {
        this.today.is_check_in = this.today.is_check_in = (this.type >= 3);        
        this.showSwitch = this.today.is_check_in;
    },
    mounted: function () {
        const obj = {
            'user_id': parseInt(this.user_id),
            'name': -1,
            'start': -1,
            'end': -1,
            'status': -1,
            'order': [['m_date'], ['DESC']]
        };
        if (this.type >= 3) {
            obj['d_id'] = -1;
        } else {
            obj['d_id'] = parseInt(this.department);
            this.fetchData(obj, true);
        }
        if (this.type >= 2) {
            obj['user_id'] = -1;
            this.fetchData(obj, false);
        }
        this.showSelfData = this.selfData.slice(0, this.showNum);
        this.showAllData = this.allData.slice(0, this.showNum);
    }
};
</script>

<style scoped>
.table-style{
      display: inline;
      align-items: center;
}
</style>
