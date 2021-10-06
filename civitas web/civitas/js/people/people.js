//个人详情组件
Vue.component("people-detail", {
    props: ["prop","uid"],
    data: function () {
        return {
            friend: false,
            friend_level: ""
        }
    },
    created: function () {
        document.title = this.prop.username + "的主页 - 古典社会模拟 CIVITAS2";
        this.is_friend();
    },
    watch: {
        prop: {
            handler: function () {
                document.title = this.prop.username + "的主页 - 古典社会模拟 CIVITAS2";
            },
            deep: true
        }
    },
    methods: {
        is_friend: function () {
            var vm = this;
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/isfriend/",
                withCredentials: true,
                params: {
                    uid: this.prop.uid,
                },
            })
            .then(function (response) {
                var datas = response.data;
                if (datas.message == "你们是好友") {
                    vm.friend = true;
                    vm.friend_level = "点头之交";
                }
                else if (datas.message == "你们还不是好友") {
                    vm.friend = false;
                }
            })
            .catch(function (error) {
                console.log(error);
            })
        },
        add_friend: function () {
            var vm = this;
            var post_data = new URLSearchParams();
            post_data.append("uid",this.prop.uid);
            axios({
                method: "post",
                url: "https://api.trickydeath.xyz/addfriend/",
                withCredentials: true,
                data: post_data
            })
            .then(function (response) {
                var datas = response.data;
                if (datas.message == "添加好友成功") {
                    vm.is_friend();
                }
            })
            .catch(function (error) {
                console.log(error);
            })
        }
    },
    template:`
    <div class="people-detail">
        <img v-bind:src="'https://api.trickydeath.xyz/getavatar/?uid='+prop.uid" class="img-thumbnail" width="100px" height="100px">
        <div class="people-text">
            <p>{{ prop.username }}</p>
            <p class="explain">>位于<a v-bind:href="'city.html?uid='+prop.cityid">京兆尹</a>，长安县 >籍贯<a v-bind:href="'city.html?uid='+prop.cityid">京兆尹</a></p>
            <p class="explain">><a v-bind:href="'depository.html?uid='+prop.uid">{{ prop.username }}的库房</a></p>
        </div>
        <div class="people-add-friend" v-if="prop.uid != uid">
            <button class="btn btn-sm" v-on:click="add_friend" v-if="friend == false">添加好友+</button>
            <button class="btn btn-sm" v-else-if="friend == true">{{ friend_level }}x</button>
        </div>
    </div>
    `
})

//社交记录组件
Vue.component("people-social", {
    props: ["prop","uid","type"],
    data: function () {
        return {
            socials: [],
            length: 0,
            page: 1,
            friend: false,
        }
    },
    created: function () {
        this.is_friend();
        this.get_social();
        if (this.type == "total") {
            document.title = this.prop.username + "的社交记录 - 古典社会模拟 CIVITAS2"
        }
    },
    watch: {
        prop: {
            handler: function () {
                if (this.type == "total") {
                    document.title = this.prop.username + "的社交记录 - 古典社会模拟 CIVITAS2"
                }
            },
            deep: true
        }
    },
    methods: {
        get_social: function () {
            var vm = this;
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getsocial/",
                withCredentials: true,
                params: {
                    uid: this.prop.uid,
                    page: this.page
                },
            })
            .then(function (response) {
                var datas = response.data.data;
                vm.socials = datas.datalist;
                if (vm.socials.length >= 5 && vm.type == "people") {
                    vm.length = 5;
                }
                else {
                    vm.length = vm.socials.length;
                }
            })
            .catch(function (error) {
                console.log(error);
            })
        },
        is_friend: function () {
            var vm = this;
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/isfriend/",
                withCredentials: true,
                params: {
                    uid: this.prop.uid,
                },
            })
            .then(function (response) {
                var datas = response.data;
                if (datas.message == "你们是好友") {
                    vm.friend = true;
                }
                else if (datas.message == "你们还不是好友") {
                    vm.friend = false;
                }
            })
            .catch(function (error) {
                console.log(error);
            })
        },
        do_social_behavior: function (type) {
            var vm = this;
            var post_data = new URLSearchParams();
            post_data.append("type",type);
            post_data.append("uid",this.prop.uid);
            post_data.append("message","");
            axios({
                method: "post",
                url: "https://api.trickydeath.xyz/socialbehavior/",
                withCredentials: true,
                data: post_data
            })
            .then(function (response) {
                vm.get_social();
                main_vm.get_status();
            })
            .catch(function (error) {
                console.log(error);
            })
        }
    },
    template:`
    <div class="social-total">
        <p class="main-char">{{ prop.username }}的社交关系</p>
        <div class="social-methods bottomline-dashed" v-if="type == 'people'">
            <p class="explain" v-if="prop.uid == uid">你不能对自己进行社交。</p>
            <p class="explain" v-else-if="friend == false">
                你还不是{{ prop.username }}的好友，但你可以
                <a href="javascript:void(0)" v-on:click="do_social_behavior(1)">公开谴责</a>。
            </p>
            <p class="explain" v-else-if="friend == true">
                你和{{ prop.username }}是好友。<br>
                <a href="javascript:void(0)" v-on:click="do_social_behavior(0)">公开赞扬</a>
                <a href="javascript:void(0)" v-on:click="do_social_behavior(1)">公开谴责</a>
                <a href="javascript:void(0)" v-on:click="do_social_behavior(2)">私下表扬</a>
                <a href="javascript:void(0)" v-on:click="do_social_behavior(3)">私下批评</a>
                <a href="javascript:void(0)" v-on:click="do_social_behavior(4)">赠送礼物</a>
            </p>
        </div>
        <div class="social-detail">
            <p class="explain" v-if="socials.length == 0">{{ prop.username }}还没有社交记录。</p>
            <template v-else>
                <div class="social-single bottomline-dashed" v-for="(social,index) in socials.slice(0,length)" v-bind:key="index">
                    <a v-bind:href="'people.html?uid='+social.from_person_uid">
                        <img v-bind:src="'https://api.trickydeath.xyz/getavatar/?uid='+social.from_person_uid" class="img-thumbnail" width="50px" height="50px">
                    </a>
                    <p>
                        <a v-bind:href="'people.html?uid='+social.from_person_uid">{{ social.from_person_username }}</a> {{ social.social_type }}了
                        <a v-bind:href="'people.html?uid='+social.to_person_uid">{{ social.to_person_username }}</a>。<br>
                        第{{ social.day }}天，{{ social.time }}。
                    </p>
                    <a v-bind:href="'people.html?uid='+social.to_person_uid">
                        <img v-bind:src="'https://api.trickydeath.xyz/getavatar/?uid='+social.to_person_uid" class="img-thumbnail" width="50px" height="50px">
                    </a>
                </div>
            </template>
            <div class="social-more" v-if="type == 'people'">
                <a v-bind:href="'social.html?uid='+prop.uid">>>查看更多社交记录</a>
            </div>
        </div>
    </div>
    `
})

//好友显示组件
Vue.component("people-friend", {
    props: ["prop"],
    data: function () {
        return {
            friends: [],
            length: 0,
            page: 1,
        }
    },
    created: function () {
        this.get_friend();
    },
    methods: {
        get_friend: function () {
            var vm = this;
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getfriend/",
                withCredentials: true,
                params: {
                    page: this.page
                },
            })
            .then(function (response) {
                var datas = response.data.data;
                vm.friends = datas.datalist;
            })
            .catch(function (error) {
                console.log(error);
            })
        }
    },
    template:`
    <div class="social-total">
        <p class="main-char">我的人际关系</p>
        <p class="explain" v-if="friends.length == 0">你还没有好友。</p>
        <template v-else>
            <div class="social-single bottomline-dashed" v-for="(friend,index) in friends" v-bind:key="index">
                <a v-bind:href="'people.html?uid='+friend.friend_uid">
                    <img v-bind:src="'https://api.trickydeath.xyz/getavatar/?uid='+friend.friend_uid" class="img-thumbnail" width="50px" height="50px">
                </a>
                <p>
                    <a v-bind:href="'people.html?uid='+friends.friend_uid">{{ friend.friend_username }}</a><br>
                    第{{ friend.day }}天，{{ friend.time }}。
                </p>
            </div>
        </template>
    </div>
    `
})