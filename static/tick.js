

var app = new Vue({
    el: "#app",
    data: {
        contract_code: "P2005",
        start_date: "2020-01-01",
        end_date: "2020-02-22",
        now_date: "1990-02-10",
        trade_date: "",
        picture_url: "http://a3.att.hudong.com/68/61/300000839764127060614318218_950.jpg",
        ts_code: "aa",
    },
    methods: {
        get_next_picture: function () {
            if( this.now_date <= this.start_date){
                this.now_date = this.start_date;
            };
            if (this.now_date > this.end_date){
                alter("日期已循环完成");
                return null;
            };

            var that = this;

            // 获取ts_code
            // 47.92.6.148:6678 写死不好, 但是暂时不知道怎么弄到配置文件里去
            axios.get("http://47.92.6.148:6678/future/holding_info/?symbol=" + that.contract_code)
            .then(function (response) {
                that.ts_code = response.data[0][0];
                console.log(that.ts_code);

                // 获取下一个交易日
                axios.get("http://47.92.6.148:6678/future/get_next_trade_day/?data_date=" + that.now_date)
                    .then(function (response) {
                        that.trade_date = response.data;
                        console.log(response);

                    // 生成图片并获取生成的图片的地址
                    axios.get("http://47.92.6.148:6678/future/plot_future_interval_point_data_by_ts_code/?end_date=" + that.trade_date + "&ts_code=" + that.ts_code)
                        .then(function (response) {
                            that.picture_url = response.data;
                            console.log(response.data);

                            that.now_date = that.trade_date
                        }, function (err) {
                            alert(err);
                            return null;
                        })

                    }, function (err) {
                        alert(err);
                        return null;
                    })
            }, function (err) {
                alert(err);
                return null;
            })




        }
    }
})