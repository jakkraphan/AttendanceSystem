<template>
    <Row class="vm-table vm-panel">
        <div class="panel-heading"> 员工考勤 </div>
        <div class="panel-body">
            <Row type="flex" justify="space-between" class="control">
                <div class="table-style">
                    <h3  v-if="this.type >= 2">考勤/查看</h3>
                    <i-switch v-model="showSwitch" style="margin: 0 10px 0 5px"  v-if="this.type >= 2"></i-switch>
                    <Select v-model="search_department" clearable style="width:100px; margin: 0 5px;" placeholder="部门" v-if="this.type >= 2 && showSwitch">
                        <Option v-for="(value, key) of this.departments" :value="key" :key="key">{{ value }}</Option>
                    </Select>
                    <Input v-model="search_id" placeholder="工号" style="width:100px;margin: 0 5px;" v-if="this.type >= 2 && showSwitch"></Input>
                    <Input v-model="search_name" placeholder="姓名" style="width:100px;margin: 0 5px;" v-if="this.type >= 2 && showSwitch"></Input>
                    <DatePicker v-model="begintime" type="date" placeholder="起始日期" style="width: 125px; margin: 0 5px 0 0"></DatePicker>
                    <DatePicker v-model="endtime" type="date" placeholder="结束日期"  style="width: 125px; margin: 0 5px"></DatePicker>         
                    <Button type="ghost" style="margin: 0 10px 0 10px" @click="deepSearch">Deep Search</Button>
                </div>
                <div class="search-bar">
                    <Input placeholder="Please enter ..." v-model="keyword" style="width: 200px"></Input>
                    <Button type="ghost" @click="search" icon="search"></Button>
                </div>
            </Row>
            <div class="edit" v-if="this.showSwitch">
                <Button @click="add" icon="plus-round" v-if="this.type === 4">添加</Button>
                <Button  :disabled="deleteDisabled" @click="modalDelete = true" icon="trash-a" v-if="this.type === 4">删除</Button>
            </div>
            <div class="edit" v-else>
                <Tag type="dot" color="blue">{{this.date}}</Tag>                
                <Button @click="checkin" style="width: 100px;margin: 0 5px">签到</Button>
                <Button @click="checkout" style="width: 100px;margin: 0 5px">签退</Button>
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
        
    </Row>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    name: 'attendance',
    data () {
        return {
            date: this.formatDate(new Date()),
            begintime: '',
            endtime: '',
            deleteDisabled: true,
            search_department: '',
            search_id: '',
            search_name: '',
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
                        return h(text);
                    }
                }
            ],
            status: [
                '未定', '迟到', '早退', '迟到早退', '不正常上班', '缺勤', '正常', '请假', '出差'
            ]
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
                    'm_date': this.dataEdit['date']
                },
                'args': {
                    'check_in_time': this.dataEdit['begintime'],
                    'check_out_time': this.dataEdit['endtime'],
                    'status': this.dataEdit['status']
                }
            };
            this.$socket.emit('update', obj, function (status) {
                if (status) {
                    that.allData.forEach(elem => {
                        if (elem['user_id'] === that.dataEdit['user_id'] && elem['date'] === that.dataEdit['']) {
                            for (let i in that.dataEdit) {
                                elem[i] = that.dataEdit[i];
                            }
                        }
                    });
                } else {
                    this.$Message.error('编辑失败');
                }
            });
        },
        addOk: function () {
            const that = this;
            const obj = {
                'table': 'attendance_table',
                'args': {
                    'user_id': this.dataAdd['user_id'],
                    'm_date': this.dataAdd['date'],
                    'check_in_time': this.dataAdd['begintime'],
                    'check_out_time': this.dataAdd['endtime'],
                    'status': this.dataAdd['status']
                }
            };
            this.$socket.emit('insert', obj, function (status) {
                if (status) {
                    that.allData.unshift(this.dataAdd);
                } else {
                    this.$Message.error('插入失败');
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

        },
        checkout: function () {

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
                'status': -1,
                'order': [['user_id'], ['ASC']]
            };
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
            if (this.begintime !== '') {
                obj['start'] = this.begintime;
            } else {
                obj['start'] = -1;
            }
            if (this.endtime !== '') {
                obj['end'] = this.endtime;
            } else {
                obj['end'] = -1;
            }
            this.fetchData(obj);
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
                        this.dataEdit = true;
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
        fetchData: function (obj, isSelf) {
            const that = this;
            this.$socket.emit('attendance_search', obj, function (...args) {
                if (args !== undefined) {
                    let data2push = [];
                    for (let i of args) {
                        data2push.push({
                            'used_id': i[0],
                            'date': i[1],
                            'begintime': i[2],
                            'endtime': i[3],
                            'status': i[4]
                        });
                    }
                    if (isSelf) {
                        that.selfData = data2push;
                    } else {
                        that.allData = data2push;
                    }
                } else {
                    that.$Message.error('失败');
                }
            });
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
    mounted: function () {
        const obj = {
            'name': -1,
            'start': -1,
            'end': -1,
            'status': -1,
            'order': [['user_id'], ['ASC']]
        };
        if (this.type >= 3) {
            obj['d_id'] = -1;
        } else {
            obj['d_id'] = this.department;
        }
        this.fetchData(obj);
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
