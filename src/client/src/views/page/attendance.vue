<template>
    <div>
        <div class="top">
            <Card>
                <p slot="title">{{date}}</p>
                    <p>
                        <Button type="primary" class="btn left" size="large">{{check_in}}</Button>
                        <Button type="primary" class="btn right" size="large">{{check_out}}</Button>
                    </p>
            </Card>
        </div>
        <Table :data="self_data" :columns="self_cols" stripe></Table>
        <div style="margin: 10px;overflow: hidden">
            <div style="float: right;">
                <Page :total="100" :current="1" @on-change="changePage"></Page>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'attendance',
    data () {
        return {
            date: this.formatDate(new Date()),
            is_checkin: false,
            is_checkout: false,
            self_cols: [
                {
                    title: 'Date',
                    key: 'date',
                    sortable: true
                },
                {
                    title: 'CheckIn',
                    key: 'chechin',
                    render: (h, params) => {
                        const row = params.row;
                        let color, text;
                        if (row.checkin === 1) {
                            color = 'blue';
                            text = '已签到';
                        } else if (row.checkin === 2) {
                            color = 'yellow';
                            text = '迟到';
                        } else {
                            color = 'red';
                            text = '未签到';
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
                    title: 'CheckOut',
                    key: 'checkout',
                    render: (h, params) => {
                        const row = params.row;
                        let color, text;
                        if (row.checkout === 1) {
                            color = 'blue';
                            text = '已签退';
                        } else if (row.checkout === 2) {
                            color = 'yellow';
                            text = '早退';
                        } else {
                            color = 'red';
                            text = '未签退';
                        }

                        return h('Tag', {
                            props: {
                                type: 'dot',
                                color: color
                            }
                        }, text);
                    }
                }
            ],
            self_data: this.mock()
        };
    },
    methods: {
        mock () {
            let data = [];
            for (let i = 0; i < 10; i++) {
                data.push({
                    date: this.formatDate(new Date()),
                    checkin: Math.floor(Math.random() * 3 + 1),
                    checkout: Math.floor(Math.random() * 3 + 1)
                });
            }
            return data;
        },
        formatDate (date) {
            const y = date.getFullYear();
            let m = date.getMonth() + 1;
            m = m < 10 ? '0' + m : m;
            let d = date.getDate();
            d = d < 10 ? ('0' + d) : d;
            return y + '-' + m + '-' + d;
        },
        changePage () {
            this.self_data = this.mock();
        }
    },
    computed: {
        check_in () {
            return this.is_checkin ? '已签到' : '签到';
        },
        check_out () {
            return this.is_checkout ? '已签退' : '签退';
        }
    }
};
</script>

<style scoped>

.btn {
    width: 45%;
}

.top {
    margin-bottom: 1%;
}

.right {
    float: right;
}
</style>
