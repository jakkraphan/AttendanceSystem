<template>
    <Row class="vm-table vm-panel">
        <div class="panel-heading"> 请假申请 </div>
        <div class="panel-body">
            <Row type="flex" justify="space-between" class="control">
                <div class="table-style">
                    <DatePicker v-model="begindate" type="date" placeholder="起始日期" style="width: 125px; margin: 0 5px 0 0"></DatePicker>
                    <DatePicker v-model="enddate" type="date" placeholder="结束日期"  style="width: 125px; margin: 0 5px"></DatePicker>          
                    <Select v-model="search_department" clearable style="width:100px; margin: 0 5px;" placeholder="部门" v-if="type >= 3">
                        <Option v-for="(value, key) of this.departments" :value="key" :key="key">{{ value }}</Option>
                    </Select>
                    <Input v-model="search_id" placeholder="工号" style="width:100px;margin: 0 5px 0 5px;" v-if="type>=2"></Input>
                    <Input v-model="search_name" placeholder="姓名" style="width:100px;margin: 0 5px;" v-if="type>=2"></Input>
                    <Input-number :max="99" :step="1" v-model="days.min" style="width:50px; margin: 0 5px;"></Input-number>
                    <Input-number :max="99" :step="1" v-model="days.max" style="width:50px; margin: 0 5px;"></Input-number>      
                    <Button type="ghost" style="margin: 0 5px" @click="deepSearch">Deep Search</Button>
                </div>
                <div class="search-bar">
                    <Input placeholder="Please enter ..." v-model="keyword" style="width: 200px"></Input>
                    <Button type="ghost" @click="search" icon="search"></Button>
                </div>
            </Row>
            <div class="edit">
                <Button @click="modalAdd = true" icon="plus-round"  v-if="type === 1 || type >= 4">添加</Button>
                <Button  :disabled="deleteDisabled" @click="modalDelete = true" icon="trash-a"  v-if="type >= 4">删除</Button>
                <Tag type="dot" color="blue" style="margin: 0 5px 0 20px;">查询顺序</Tag>
                <Checkbox-group v-model="korder" style="display: inline;">
                    <Checkbox label="leave_table.user_id">
                        <span>员工工号</span>
                    </Checkbox>
                    <Checkbox label="d_id">
                        <span>部门编号</span>
                    </Checkbox>
                    <Checkbox label="m_type">
                        <span>请假类型</span>
                    </Checkbox>
                    <Checkbox label="status">
                        <span>申请状态</span>
                    </Checkbox>
                </Checkbox-group>
                <template v-for="i in korder.length">
                    <Select v-model="vorder[i-1]" style="width:100px; margin: 0 5px;" :key="i">
                        <Option v-for="item in vorderv" :value="item.value" :key="item">{{ item.label }}</Option>
                    </Select>
                </template>
            </div>
            <Table :columns="showColumns" :data="showData" @on-selection-change="selectChange"></Table>
            <Row type="flex" justify="space-between" class="footer">
                <div class="info-bar">
                    Show<Input-number class="input-number" v-model="showNum" :max="leaveData.length" :min="1" @on-change="updataShowData ">{{ showNum }}</Input-number>/ Page
                </div>
                <div class="page">
                <span class="total">Total {{ leaveData.length }}</span>
                <Page :total="leaveData.length" :current="currentPage" :page-size="showNum" @on-change="pageChange"></Page>
                </div>
            </Row>
        </div>
    
        <Modal
            v-model="modalEdit"
            title="Edit"
            ok-text="OK"
            cancel-text="Cancel"
            @on-ok="editOk">
            <Form :label-width="80" :ref="dataEdit" :model="dataEdit">
                <Form-item label="开始日期">
                    <DatePicker v-model="dataEdit['begintime']" type="date" placeholder="请选择开始日期" label="开始日期"></DatePicker>
                </Form-item>
                <Form-item label="结束日期">                
                    <DatePicker v-model="dataEdit['endtime']" type="date" placeholder="请选择结束日期" label="结束日期"></DatePicker>
                </Form-item>
                <Form-item label="请假类型">                
                     <Select v-model="dataEdit['type']">
                        <Option v-for="(item, index) in apply_type" :value="index" :key="item">{{ item }}</Option>
                    </Select>
                </Form-item>
                <Form-item label="请假理由">
                    <Input v-model="dataEdit['reason']" type="textarea" placeholder="请输入请假理由" label="请假理由"></Input>
                </Form-item>
                <Form-item label="申请状态"  v-if="this.type >= 4">
                    <Select v-model="dataEdit['status']">
                        <Option v-for="(item, index) in passed" :value="index" :key="item">{{ item }}</Option>
                    </Select>
                </Form-item>    
                <Form-item label="拒绝理由" v-if="type >= 4">
                    <Input v-model="dataEdit['reply']" type="textarea" placeholder="请输入拒绝理由" label="拒绝理由"></Input>
                </Form-item>
            </Form>
        </Modal>
        <Modal 
            v-model="modalReply"
            title="Reply"
            ok-text="OK"
            cancel-text="Cancel"
            @on-ok="replyOk">
            <Form :label-width="80" ref="dataEdit" :model="dataEdit">
                <Form-item label="拒绝理由">
                    <Input v-model="dataEdit['reply']" type="textarea" placeholder="请输入拒绝理由" label="拒绝理由"></Input>
                </Form-item>
            </Form>
        </Modal>
        <Modal
            v-model="modalAdd"
            title="Add"
            ok-text="OK"
            cancel-text="Cancel"
            @on-ok="addOk">
            <Form :label-width="80" ref="dataAdd" :model="dataAdd">
                <Form-item label="员工工号" v-if="this.type >= 4">
                    <Input v-model="dataAdd['user_id']" placeholder="请输入工号" label="员工工号"></Input>                
                </Form-item>
                <Form-item label="开始日期">
                    <DatePicker v-model="dataAdd['begintime']" type="date" placeholder="请选择开始日期" label="开始日期"></DatePicker>
                </Form-item>
                <Form-item label="结束日期">
                    <DatePicker v-model="dataAdd['endtime']" type="date" placeholder="请选择结束日期" label="结束日期"></DatePicker>
                </Form-item>
                <Form-item label="请假类型">              
                    <Select v-model="dataAdd['type']">
                        <Option v-for="(item, index) in apply_type" :value="index" :key="item">{{ item }}</Option>
                    </Select>
                </Form-item>
                <Form-item label="请假理由">
                    <Input v-model="dataAdd['reason']" type="textarea" placeholder="请输入请假理由" label="请假理由"></Input>                         
                </Form-item>
                <Form-item label="申请状态"  v-if="this.type === 4">
                     <Select v-model="dataAdd['status']">
                        <Option v-for="(item, index) in passed" :value="index" :key="item">{{ item }}</Option>
                    </Select>
                </Form-item>    
                <Form-item label="拒绝理由" v-if="this.type === 4">
                    <Input v-model="dataEdit['reply']" type="textarea" placeholder="请输入拒绝理由" label="拒绝理由"></Input>
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
import Util from '../../libs/util';

export default {
    name: 'leave',
    data () {
        return {
            deleteDisabled: true,
            showData: [],
            showNum: 10,
            currentPage: 1,
            keyword: '',
            search_department: '',
            search_id: '',
            search_name: '',
            begindate: '',
            enddate: '',
            days: {
                min: -1,
                max: -1
            },
            modalEdit: false,
            modalAdd: false,
            modalReply: false,
            modalDelete: false,
            dataEdit: {},
            dataDelete: [],
            dataAdd: {},
            leaveData: [],
            leaveColumns: [
                {
                    title: '编号',
                    key: 'number',
                    sortable: true
                },
                {
                    title: '工号',
                    key: 'user_id',
                    sortable: true
                },
                {
                    title: '开始时间',
                    key: 'begintime',
                    sortable: true
                },
                {
                    title: '结束时间',
                    key: 'endtime',
                    sortable: true
                },
                {
                    title: '请假类型',
                    key: 'type',
                    sortable: true,
                    render: (h, params) => {
                        const row = params.row;
                        let text = this.apply_type[row.type];
                        return h('Tag', {
                            props: {
                            }
                        }, text);
                    }
                },
                {
                    title: '理由',
                    key: 'reason'
                },
                {
                    title: '状态',
                    key: 'status',
                    sortable: true,
                    render: (h, params) => {
                        const row = params.row;
                        let text = this.passed[row.status];
                        return (text);
                    }
                },
                {
                    title: '回复',
                    key: 'reply'
                }
            ],
            keys: ['number', 'user_id', 'begintime', 'endtime', 'reason', 'reply', 'type', 'status'],
            passed: ['已保存', '已提交', '已通过', '未通过'],
            apply_type: ['事假', '病假', '产假', '婚假'],
            korder: [],
            vorder: ['ASC', 'ASC', 'ASC', 'ASC'],
            vorderv: [{ value: 'ASC', label: '顺序' }, {value: 'DESC', label: '逆序'}]
        };
    },
    methods: {
        editOk: function () {
            const data = this.dataEdit;
            const obj = {
                table: 'leave_table',
                log: 'modify_leave',
                key: {'number': data['number']},
                args: {
                    'user_id': data['user_id'],
                    'begin_time': Util.formatDate(data['begintime']),
                    'end_time': Util.formatDate(data['endtime']),
                    'reason': data['reason'],
                    'reply': data['reply'],
                    'm_type': data['type'],
                    'status': data['status']
                }
            };
            if (this.type <= 1) {
                obj['args']['status'] = 0;
            }
            this.updateData(obj);
        },
        replyOk: function () {
            const data = this.dataEdit;
            if (data['reply'] === '') {
                this.$Message.error('回复不能为空');
                return;
            }
            const obj = {
                table: 'leave_table',
                log: 'reject_leave',
                key: {'number': data['number']},
                args: {
                    'status': 3,
                    'reply': data['reply']
                }
            };
            this.updateData(obj);
        },
        submit: function () {
            const data = this.dataEdit;
            const obj = {
                table: 'leave_table',
                key: {
                    'number': data['number']
                },
                log: 'submit_leave',
                args: {
                    'status': 1
                }
            };
            this.updateData(obj);
        },
        pass: function () {
            const data = this.dataEdit;
            const obj = {
                table: 'leave_table',
                log: 'approve_leave',
                key: {
                    'number': data['number']
                },
                args: {
                    status: 2
                }
            };
            this.updateData(obj);
        },
        addOk: function () {
            const data = this.dataAdd;
            const obj = {
                table: 'leave_table',
                log: 'add_leave',
                args: {
                    'user_id': data['user_id'],
                    'begin_time': data['begintime'],
                    'end_time': data['endtime'],
                    'reason': data['reason'],
                    'reply': data['reply'],
                    'm_type': data['type'],
                    'status': data['status']
                }
            };
            if (this.dataAdd['user_id'] === undefined) {
                obj.args['user_id'] = this.user_id;
                obj.args['status'] = 1;
            }
            this.insertData(obj);
        },
        deleteOk: function () {
            const data = this.dataDelete;
            const that = this;
            const args = {};
            const obj = {
                table: 'leave_table',
                log: 'del_leave',
                args: args
            };
            for (let item in data) {
                args['number'] = item['number'];
                this.$socket.emit('delete', obj, function (status) {
                    if (status) {
                        that.leaveData = that.leaveData.filter(i => i['number'] !== item['number']);
                    } else {
                        that.$Message.error('删除失败');
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
            this.showData = this.leaveData.slice(startPage, endPage);
        },
        search: function () {
            let that = this;
            let tempData = that.leaveData;
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
        deepSearch: function () {
            const obj = {
                'table': 'leave_table',
                'user_id': -1,
                'd_id': -1,
                'name': -1,
                'start': -1,
                'end': -1,
                'type': -1,
                'days': this.days,
                'status': -1,
                'order': [['leave_table.user_id'], ['ASC']]
            };
            if (this.begindate !== '') {
                obj['start'] = this.begindate;
            }
            if (this.enddate !== '') {
                obj['end'] = this.enddate;
            }
            if (this.search_name !== '') {
                obj['name'] = this.search_name;
            }
            if (this.search_id !== '') {
                obj['user_id'] = parseInt(this.search_id);
            }
            if (this.search_department !== '') {
                obj['d_id'] = parseInt(this.search_department);
            }
            if (this.korder.length > 0) {
                const newVorder = this.vorder.slice(0, this.korder.length);
                obj['order'] = [this.korder, newVorder];
            }
            this.fetchData(obj);
        },
        selectChange: function (data) {
            this.dataDelete = data;
        },
        remove: function (index) {
            this.showData.splice(index, 1);
        },
        renderOperate: function (h, params) {
            const row = params.row;
            if (row.status === 2 && this.type < 4) {
                return h('div', [h('Button', {
                    props: {
                        type: 'success',
                        size: 'small'
                    },
                    style: {
                        marginRight: '5px'
                    }
                }, '已经通过')]);
            } else if (row.status === 3 && this.type < 4 && this.type > 2) {
                return h('div', [h('Button', {
                    props: {
                        type: 'error',
                        size: 'small'
                    },
                    style: {
                        marginRight: '5px'
                    }
                }, '未获通过')]);
            } else {
                let btn = [[], []];
                if (this.type === '1' || this.type === 1) {
                    btn[0] = ['info', '编辑'];
                    btn[1] = ['warning', '提交'];
                } else if (this.type === '2' || this.type === 2) {
                    btn[0] = ['error', '拒绝'];
                    btn[1] = ['success', '通过'];
                } else if (this.type >= 4) {
                    btn[0] = ['info', '编辑'];
                    btn[1] = ['error', '删除'];
                }

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

                            if (this.type <= 1 || this.type >= 4) {
                                this.modalEdit = true;
                            } else {
                                this.modalReply = true;
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
                            if (this.type === 1 | this.type === '1') {
                                this.dataEdit['number'] = params.row['number'];
                                this.submit();
                            } else if (this.type === 2 || this.type === '2') {
                                this.dataEdit['number'] = params.row['number'];
                                this.pass();
                            } else if (this.type >= 4) {
                                this.dataDelete.push(params.row);
                                this.modalDelete = true;
                            }
                        }
                    }
                }, btn[1][1]);

                return h('div', [btn1, btn2]);
            }
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
        fetchData: function (obj) {
            const that = this;
            this.$socket.emit('tl_search', obj, function (...args) {
                if (args !== undefined && args.length > 0) {
                    that.leaveData = [];
                    for (let i of args[0]) {
                        if (that.type !== '2' || i[7] > 0) {
                            that.leaveData.push({
                                'number': i[0],
                                'user_id': i[1],
                                'begintime': i[2],
                                'endtime': i[3],
                                'reason': i[4],
                                'reply': i[5],
                                'type': i[6],
                                'status': i[7]
                            });
                        }
                    }
                } else {
                    that.$Message.error('查询失败');
                }
            });
        },
        updateData (data) {
            const that = this;
            this.$socket.emit('update', data, function (status) {
                if (status) {
                    that.fetchAllData();
                } else {
                    that.$Message.error('编辑失败');
                }
            });
        },
        insertData (data) {
            const that = this;
            this.$socket.emit('insert', data, function (ret) {
                if (ret) {
                    that.fetchAllData();
                } else {
                    that.$Message.error('添加失败');
                }
            });
        },
        fetchAllData () {
            const obj = {
                'table': 'leave_table',
                'user_id': -1,
                'd_id': -1,
                'name': -1,
                'start': -1,
                'end': -1,
                'type': -1,
                'days': {
                    'min': -1,
                    'max': -1
                },
                'status': -1,
                'order': [['leave_table.user_id'], ['ASC']]
            };
            if (this.type <= 2) {
                obj['d_id'] = this.department;
            }
            if (this.type === '1' || this.type === 1) {
                obj['user_id'] = this.user_id;
                obj['order'] = [['user_id'], ['ASC']];
            }
            this.fetchData(obj);
        }
    },
    computed: {
        ...mapGetters([
            'user_id',
            'type',
            'department',
            'departments'
        ]),
        showColumns: function () {
            let showColumn = this.leaveColumns.slice();
            if (this.type <= 2 || this.type >= 4) {
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
        }
    },
    watch: {
        leaveData: function () {
            this.showData = this.leaveData.slice(0, this.showNum);
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
        this.fetchAllData();
        this.showData = this.leaveData.slice(0, this.showNum);
    }
};
</script>