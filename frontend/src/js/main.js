/**
 * Created by shuai on 7/24/2018.
 */


var main = new Vue({
    el: "#myTabContent",
    data: {
        object: [],
        uid: ''
    },
    created(){
        this.selectInfo()
    },
    methods: {
        getUserName: function(docker_name){
            this.docker_name = docker_name;
        },
        selectInfo: function(dire, uid){
            console.log(dire, uid)
            var _this = this
            axios.get('/info', {
                params:{
                    'dire': dire,
                    'uid': uid
                }
            })
            .then(function (response) {
                ret = response.data;
                console.log(ret)
                if (ret['code'] == 0){
                    _this.object = ret['msg']
                    _this.uid = ret['uid']
                }
            })
            .catch(function (error) {
                console.log(error);
            });
        }
    }
})

