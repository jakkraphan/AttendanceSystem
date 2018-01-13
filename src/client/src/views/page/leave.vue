<template>
    <Row class="vm-table vm-panel">
        <div class="panel-heading"> 请假申请 </div>
        <div class="panel-body">
            <Row type="flex" justify="space-between" class="control">
                <div class="table-style">
                    <DatePicker v-model="begindate" type="date" placeholder="起始日期" style="width: 125px; margin: 0 5px 0 0"></DatePicker>
                    <DatePicker v-model="enddate" type="date" placeholder="结束日期"  style="width: 125px; margin: 0 5px"></DatePicker>          
                    <Select v-model="search_department" clearable style="width:100px; margin: 0 5px;" placeholder="部门" v-if="this.type>=3">
                        <Option v-for="(value, key) of this.departments" :value="key" :key="key">{{ value }}</Option>
                    </Select>
                    <Input v-model="search_id" placeholder="工号" style="width:100px;margin: 0 5px 0 5px;" v-if="this.type>=2"></Input>
                    <Input v-model="search_name" placeholder="姓名" style="width:100px;margin: 0 5px;" v-if="this.type>=2"></Input>
                    <Button type="ghost" style="margin: 0 5px" @click="deepSearch">Deep Search</Button>
                </div>
                <div class="search-bar">
                    <Input placeholder="Please enter ..." v-model="keyword" style="width: 200px"></Input>
                    <Button type="ghost" @click="search" icon="search"></Button>
                </div>
            </Row>
            <div class="edit" v-if="type === 1 || type === 4">
                <Button @click="modalAdd = true" icon="plus-round">添加</Button>
                <Button  :disabled="deleteDisabled" @click="modalDelete = true" icon="trash-a">删除</Button>
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
                    <DatePicker v-model="dataEdit['begindate']" type="date" placeholder="请选择开始日期" label="开始日期"></DatePicker>
                </Form-item>
                <Form-item label="结束日期">                
                    <DatePicker v-model="dataEdit['enddate']" type="date" placeholder="请选择结束日期" label="结束日期"></DatePicker>
                </Form-item>
                <Form-item label="请假类型">                
                    <RadioGroup v-model="dataEdit['type']" type="button" label="请假类型">
                        <Radio label="1">事假</Radio>
                        <Radio label="2">病假</Radio>
                        <Radio label="3">产假</Radio>
                        <Radio label="4">婚假</Radio>
                    </RadioGroup>
                </Form-item>
                <Form-item label="请假理由">
                    <Input v-model="dataEdit['reason']" type="textarea" placeholder="请输入请假理由" label="请假理由"></Input>
                </Form-item>
                <Form-item label="申请状态"  v-if="this.type === 4">
                    <RadioGroup v-model="dataEdit['status']" type="button" label="申请状态">
                        <Radio label="1">已保存</Radio>
                        <Radio label="2">已提交</Radio>
                        <Radio label="3">已通过</Radio>
                        <Radio label="4">未通过</Radio>                
                    </RadioGroup>
                </Form-item>    
                <Form-item label="拒绝理由" v-if="this.type === 4">
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
                <Form-item label="员工工号" v-if="this.type === 4">
                    <Input v-model="dataAdd['user_id']" placeholder="请输入工号" label="请假理由"></Input>                
                </Form-item>
                <Form-item label="开始日期">
                    <DatePicker v-model="dataAdd['begindate']" type="date" placeholder="请选择开始日期" label="开始日期"></DatePicker>
                </Form-item>
                <Form-item label="结束日期">
                    <DatePicker v-model="dataAdd['enddate']" type="date" placeholder="请选择结束日期" label="结束日期"></DatePicker>
                </Form-item>
                <Form-item label="请假类型">
                    <RadioGroup v-model="dataAdd['type']" type="button" label="请假类型">
                        <Radio label="1">事假</Radio>
                        <Radio label="2">病假</Radio>
                        <Radio label="3">产假</Radio>
                        <Radio label="4">婚假</Radio>
                    </RadioGroup>
                </Form-item>
                <Form-item label="请假理由">
                    <Input v-model="dataAdd['reason']" type="textarea" placeholder="请输入请假理由" label="请假理由"></Input>                         
                </Form-item>
                <Form-item label="申请状态"  v-if="this.type === 4">
                    <RadioGroup v-model="dataEdit['status']" type="button" label="申请状态">
                        <Radio label="1">已保存</Radio>
                        <Radio label="2">已提交</Radio>
                        <Radio label="3">已通过</Radio>
                        <Radio label="4">未通过</Radio>                
                    </RadioGroup>
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
                        let text;
                        if (row.type === 1) {
                            text = '事假';
                        } else if (row.type === 2) {
                            text = '病假';
                        } else if (row.type === 3) {
                            text = '产假';
                        } else if (row.type === 4) {
                            text = '婚假';
                        }

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
                        let color, text;
                        switch (row.status) {
                            case 1: {
                                color = 'grey';
                                text = '已保存';
                                break;
                            }
                            case 2: {
                                color = 'yellow';
                                text = '已提交';
                                break;
                            }
                            case 3: {
                                color = 'green';
                                text = '已通过';
                                break;
                            }
                            case 4: {
                                color = 'red';
                                text = '未通过';
                                break;
                            }
                        }
                        return h('Tag', {
                            props: {
                                type: 'dot',
                                color: color
                            }
                        }, text);
                    }
                },
                {
                    title: '回复',
                    key: 'reply'
                }
            ]
        };
    },
    methods: {
        editOk: function (data) {
            const key = {};
            const args = {};
            const obj = {
                table: 'leave',
                key: key,
                args: args
            };
            key['number'] = data['number'];
            const keys = ['begindate', 'enddate', 'type', 'reason'];
            for (let i in keys) {
                args[i] = this.dataEdit[i];
            }
            args['status'] = 1;
            this.$socket.emit('', obj, function (status) {
                if (status) {
                    this.leaveData.forEach(elem => {
                        if (elem.number === data.number) {
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
        replyOk: function (data) {
            const key = {};
            const args = {};
            const obj = {
                table: 'leave',
                key: key,
                args: args
            };
            key['number'] = data['number'];
            args['status'] = 4;
            args['reply'] = data['reply'];

            this.$socket.emit('', obj, function (status) {
                if (status) {
                    this.leaveData.forEach(function (elem) {
                        if (elem['number'] === data['number']) {
                            elem['status'] = 4;
                            elem['reply'] = data['reply'];
                        }
                    });
                } else {
                    this.$Message.error('回复失败');
                }
            });
        },
        addOk: function (data) {
            const args = {};
            const obj = {
                table: 'leave',
                args: args
            };
            args['number'] = data['number'];
            const keys = ['begindate', 'enddate', 'type', 'reason'];
            for (let i in keys) {
                args[i] = this.dataAdd[i];
            }
            if (this.dataAdd['user_id'] !== undefined) {
                args['user_id'] = this.dataAdd['user_id'];
            } else {
                args['user_id'] = this.user_id;
            }
            args['status'] = 1;
            this.$socket.emit('', obj, function (ret) {
                if (ret) {
                    this.leaveData.unshift(args);
                } else {
                    this.$Message.error('添加失败');
                }
            });
        },
        deleteOk: function (data) {
            const obj = {};
            obj['table'] = 'leave';
            for (let item in data) {
                const key = {};
                const args = {};
                args['number'] = item['number'];
                obj['key'] = key;
                this.$socket.emit('', obj, function (status) {
                    if (status) {
                        this.leaveData = this.leaveData.filter(i => i['number'] !== item['number']);
                    } else {
                        this.$Message.error('删除失败');
                    }
                });
            }
        },
        submit: function (data) {
            const key = {};
            const args = {};
            const obj = {
                table: 'leave',
                key: key,
                args: args
            };
            key['number'] = data['number'];
            args['status'] = 3;

            this.$socket.emit('', obj, function (status) {
                if (status) {
                    this.leaveData.forEach(function (elem) {
                        if (elem['number'] === data['number']) {
                            elem.status = 2;
                        }
                    });
                } else {
                    this.$Message.error('提交失败');
                }
            });
        },
        pass: function (data) {
            const key = {};
            const args = {};
            const obj = {
                table: 'leave',
                key: key,
                args: args
            };
            key['number'] = data['number'];
            args['status'] = 3;

            this.$socket.emit('', obj, function (status) {
                if (status) {
                    this.leaveData.forEach(function (elem) {
                        if (elem['number'] === data['number']) {
                            elem.status = 3;
                        }
                    });
                } else {
                    this.$Message.error('通过失败');
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
                'name': -1,
                'start': -1,
                'end': -1,
                'type': -1,
                'days': {
                    'min': -1,
                    'max': -1
                },
                'order': [['user_id'], ['ASC']]
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
                obj['user_id'] = this.search_id;
            }
            if (this.search_department !== '') {
                obj['d_id'] = this.search_department;
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
            if (row.status === 3 && this.type !== 4) {
                return h('div', [h('Button', {
                    props: {
                        type: 'success',
                        size: 'small'
                    },
                    style: {
                        marginRight: '5px'
                    }
                })]);
            } else {
                let btn = [[], []];
                if (this.type === 1) {
                    btn[0] = ['info', '编辑'];
                    btn[1] = ['warning', '提交'];
                } else if (this.type === 2) {
                    btn[0] = ['error', '拒绝'];
                    btn[1] = ['success', '通过'];
                } else if (this.type >= 4) {
                    btn[0] = ['error', '编辑'];
                    btn[1] = ['success', '删除'];
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

                            if (this.type === 1 || this.type === 4) {
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
                            if (this.type === 1) {
                                this.submit();
                            } else if (this.type === 2) {
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
                if (args !== undefined) {
                    that.leaveData = [];
                    for (let i of args) {
                        that.leaveData.push({
                            'user_id': i[0],
                            'date': i[1],
                            'begintime': i[2],
                            'endtime': i[3],
                            'status': i[4]
                        });
                    }
                } else {
                    that.$Message.error('查询失败');
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
        ]),
        showColumns: function () {
            let showColumn = this.leaveColumns.slice();
            if (this.type === 1 || this.type === 3 || this.type >= 4) {
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
    mounted: function () {
        const that = this;
        const obj = {
            'table': 'leave_table',
            'user_id': -1,
            'name': -1,
            'start': -1,
            'end': -1,
            'type': -1,
            'days': {
                'min': -1,
                'max': -1
            },
            'order': [['user_id'], ['ASC']]
        };
        if (this.type >= 3) {
            obj['d_id'] = -1;
            obj['user_id'] = -1;
        } else if (this.type >= 2) {
            obj['d_id'] = this.department;
            obj['user_id'] = -1;
        } else {
            obj['d_id'] = this.department;
            obj['user_id'] = this.this.user_id;
        }

        this.$socket.emit('tl_search', obj, function (...args) {
            if (args !== undefined) {
                for (let i of args) {
                    const item = {};
                    for (let j = 0; j < i.length; j++) {
                        item[this.keys[j]] = i[j];
                    }
                    that.leaveData.push(item);
                }
            } else {
                that.$Message.error('数据获取失败');
            }
        });
        this.showData = this.leaveData.slice(0, this.showNum);
    }
};
</script>