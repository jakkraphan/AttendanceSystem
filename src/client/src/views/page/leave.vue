<template>
    <VmTable title="请假申请" 
           type="edit" 
           :columns="leaveColumns" 
           :data="leaveData"
           v-on:add-ok="add"
           v-on:edit-ok="edit"
           v-on:delete-ok="deletefn"
           class="vm-margin">
  </VmTable>
</template>

<script>
import VmTable from '@/views/main-components/vm-table';
export default {
    name: 'leave',
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
            leaveColumns: [
                {
                    title: '工号',
                    key: 'user_id'
                },
                {
                    title: '开始时间',
                    key: 'begintime'
                },
                {
                    title: '结束时间',
                    key: 'endtime'
                },
                {
                    title: '出差类型',
                    key: 'type',
                    render: (h, params) => {
                        const row = params.row;
                        let text;
                        switch (row.type) {
                            case 1: {
                                text = '事假';
                                break;
                            }
                            case 2: {
                                text = '病假';
                                break;
                            }
                            case 3: {
                                text = '产假';
                                break;
                            }
                            case 4: {
                                text = '婚假';
                                break;
                            }
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
            ],
            leaveData: [
                {
                    user_id: '65416s843154',
                    begintime: '2018-01-07',
                    endtime: '2018-01-11',
                    type: 1,
                    reason: 'ass we can',
                    status: 1,
                    reply: '2333333'
                },
                {
                    user_id: '6d416sd4c54',
                    begintime: '2018-01-07',
                    endtime: '2018-01-11',
                    type: 2,
                    reason: 'ass we can',
                    status: 3,
                    reply: '2333333'
                },
                {
                    user_id: '23e22e2e2e2',
                    begintime: '2018-01-07',
                    endtime: '2018-01-11',
                    type: 2,
                    reason: 'ass we can',
                    status: 4,
                    reply: '2333333'
                },
                {
                    user_id: '6d416sd4cc4',
                    begintime: '2018-01-07',
                    endtime: '2018-01-11',
                    type: 2,
                    reason: 'ass we can',
                    status: 2,
                    reply: '23sdfssfsfsasd3333'
                },
                {
                    user_id: '65416s843154',
                    begintime: '2018-01-07',
                    endtime: '2018-01-11',
                    type: 1,
                    reason: 'ass we can',
                    status: 1,
                    reply: '2333333'
                },
                {
                    user_id: '6d416sd4c54',
                    begintime: '2018-01-07',
                    endtime: '2018-01-11',
                    type: 2,
                    reason: 'ass we can',
                    status: 3,
                    reply: '2333333'
                },
                {
                    user_id: '23e22e2e2e2',
                    begintime: '2018-01-07',
                    endtime: '2018-01-11',
                    type: 2,
                    reason: 'ass we can',
                    status: 4,
                    reply: '2333333'
                },
                {
                    user_id: '6d416sd4cc4',
                    begintime: '2018-01-07',
                    endtime: '2018-01-11',
                    type: 2,
                    reason: 'ass we can',
                    status: 2,
                    reply: '23sdfssfsfsasd3333'
                },
                {
                    user_id: '65416s843154',
                    begintime: '2018-01-07',
                    endtime: '2018-01-11',
                    type: 1,
                    reason: 'ass we can',
                    status: 1,
                    reply: '2333333'
                },
                {
                    user_id: '6d416sd4c54',
                    begintime: '2018-01-07',
                    endtime: '2018-01-11',
                    type: 2,
                    reason: 'ass we can',
                    status: 3,
                    reply: '2333333'
                },
                {
                    user_id: '23e22e2e2e2',
                    begintime: '2018-01-07',
                    endtime: '2018-01-11',
                    type: 2,
                    reason: 'ass we can',
                    status: 4,
                    reply: '2333333'
                },
                {
                    user_id: '6d416sd4cc4',
                    begintime: '2018-01-07',
                    endtime: '2018-01-11',
                    type: 2,
                    reason: 'ass we can',
                    status: 2,
                    reply: '23sdfssfsfsasd3333'
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