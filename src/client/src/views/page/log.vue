<template>
  <Row class="vm-table vm-panel">
    <div class="panel-heading"> 日志管理 </div>
    <div class="panel-body">
      <Row type="flex" justify="space-between" class="control">
        <div class="table-style">
        </div>
        <div class="search-bar">
          <Input placeholder="Please enter ..." v-model="keyword" style="width: 200px"></Input>
          <Button type="ghost" @click="search" icon="search"></Button>
        </div>
      </Row>
      <div class="edit">
          <Button @click="modalAdd = true" icon="plus-round">添加</Button>
          <Button  :disabled="deleteDisabled" @click="modalDelete = true" icon="trash-a">删除</Button>
      </div>
      <Table :columns="showColumns" :data="dataShow" @on-selection-change="selectChange"></Table>
      <Row type="flex" justify="space-between" class="footer">
        <div class="info-bar">
          Show<Input-number class="input-number" v-model="showNum" :max="logData.length" :min="1" @on-change=" updateDataShow ">{{ showNum }}</Input-number>/ Page
        </div>
        <div class="page">
          <span class="total">Total {{ logData.length }}</span>
          <Page :total="logData.length" :current="currentPage" :page-size="showNum" @on-change="pageChange"></Page>
        </div>
      </Row>
    </div>
    <Modal
        v-model="modalEdit"
        title="Edit"
        ok-text="OK"
        cancel-text="Cancel"
        on-ok="editOk">
        <Form :label-width="80">
          <Form-item v-for="(value, key) in dataEdit" :label="convertKey(key)" :key="dataEdit.id">
            <Input v-model="dataEdit[key]" :placeholder="'Please enter: ' + key"></Input>
          </Form-item>
        </Form>
    </Modal>
    <Modal
        v-model="modalAdd"
        title="Add"
        ok-text="OK"
        cancel-text="Cancel"
        on-ok="addOk">
        <Form :label-width="80">
          <Form-item v-for="item in logColumns" :label="item.title" :key="item.id">
            <Input v-model="dataAdd[item.key]" :placeholder="'Please enter: ' + item.title"></Input>
          </Form-item>
        </Form>
    </Modal>
    <Modal
        v-model="modalDelete"
        title="Delete"
        ok-text="OK"
        cancel-text="Cancel"
        on-ok="deleteOk">
        Are you sure to delete this data?
    </Modal>
  </Row>
</template>

<script>
export default {
    name: 'log',
    data () {
        return {
            deleteDisabled: true,
            dataShow: [],
            showNum: 10,
            currentPage: 1,
            keyword: '',
            modalEdit: false,
            modalAdd: false,
            modalDelete: false,
            dataEdit: {},
            dataDelete: [],
            dataAdd: {},
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
                    title: '详情',
                    key: 'info',
                    sortable: true
                }
            ],
            logData: []
        };
    },
    methods: {
        editOk: function () {
        },
        addOk: function () {
        },
        deleteOk: function () {
        },
        pageChange: function (page) {
            this.currentPage = page;
            this.updateDataShow();
        },
        updateDataShow: function () {
            let startPage = (this.currentPage - 1) * this.showNum;
            let endPage = startPage + this.showNum;
            this.dataShow = this.logData.slice(startPage, endPage);
        },
        search: function () {
            let that = this;
            let tempData = that.logData;
            that.dataShow = [];
            tempData.forEach(function (elem) {
                for (let i in elem) {
                    if (elem[i].toString().indexOf(that.keyword) > -1) {
                        that.dataShow.push(elem);
                        return;
                    };
                }
            });
        },
        selectChange: function (data) {
            this.dataDelete = data;
        },
        remove: function (index) {
            this.dataShow.splice(index, 1);
        },
        renderOperate: function (h, params) {
            const btn = [['info', '编辑'], ['error', '删除']];
            return h('div', [
                h('Button', {
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
                }, btn[0][1]),
                h('Button', {
                    props: {
                        type: btn[1][0],
                        size: 'small'
                    },
                    on: {
                        click: () => {
                            this.dataDelete.push(params.row);
                            this.modalDelete = true;
                        }
                    }
                }, btn[1][1])
            ]);
        },
        convertKey: function (value) {
            let returnValue = value;
            this.logColumns.forEach(function (elem) {
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
            let showColumn = this.logColumns.slice();
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
            return showColumn;
        }
    },
    watch: {
        logData: function () {
            this.dataShow = this.logData.slice(0, this.showNum);
        },
        dataDelete: function () {
            this.deleteDisabled = this.dataDelete.length === 0;
        }
    },
    mounted: function () {
        const that = this;
        const obj = {
            'user_id': -1,
            'order': [['user_id'], ['ASC']]
        };
        this.$socket.emit('log_search', obj, function (...args) {
            if (args !== undefined) {
                for (let i of args[0]) {
                    that.logData.push({
                        'user_id': i[0],
                        'info': i[1],
                        'datetime': i[2]
                    });
                }
            } else {
                that.$Message.error('无法获取log记录');
            }
        });
        this.dataShow = this.logData.slice(0, this.showNum);
    }
};
</script>