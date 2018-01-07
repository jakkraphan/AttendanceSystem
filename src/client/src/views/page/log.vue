<template>
  <VmTable title="操作日志" 
           type="edit" 
           :columns="logColumns" 
           :data="logData"
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
                logColumns: [
                    {
                        title: '工号',
                        key: 'user_id'
                    },
                    {
                        title: '时间',
                        key: 'datetime'
                    },
                    {
                        title: '类型',
                        key: 'type',
                        sortable: true
                    },
                    {
                        title: '详情',
                        key: 'detail',
                        sortable: false
                    }
                ],
                logData: [
                    {
                        user_id: '65416s843154',
                        datetime: '2018-01-07',
                        type: 'log',
                        detail: '23333333'
                    },
                    {
                        user_id: '6541684q6534',
                        datetime: '2018-01-07',
                        type: 'log',
                        detail: '23333333'
                    },
                    {
                        user_id: '65416843f194',
                        datetime: '2018-01-07',
                        type: 'log',
                        detail: '23333333'
                    },
                    {
                        user_id: '6541g6843150',
                        datetime: '2018-01-07',
                        type: 'log',
                        detail: '23333333'
                    },
                    {
                        user_id: '6541684q6534',
                        datetime: '2018-01-07',
                        type: 'log',
                        detail: '23333333'
                    },
                    {
                        user_id: '65416843f194',
                        datetime: '2018-01-07',
                        type: 'log',
                        detail: '23333333'
                    },
                    {
                        user_id: '6541g6843150',
                        datetime: '2018-01-07',
                        type: 'log',
                        detail: '23333333'
                    },
                    {
                        user_id: '6541684q6534',
                        datetime: '2018-01-07',
                        type: 'log',
                        detail: '23333333'
                    },
                    {
                        user_id: '65416843f194',
                        datetime: '2018-01-07',
                        type: 'log',
                        detail: '23333333'
                    },
                    {
                        user_id: '6541g6843150',
                        datetime: '2018-01-07',
                        type: 'log',
                        detail: '23333333'
                    }
                ]
            };
        }
    };
</script>

<style lang="less">
    @import '../../theme/index.less';
</style>