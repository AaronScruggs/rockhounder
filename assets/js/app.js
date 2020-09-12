var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    searchResults: [],
    showResultActions: false,
    currentPage: 0,
    totalPages: 0,
    pageSize: 5
  },
  filters: {},
  computed: {
    prevResultsBtnDisabled: function (){
      return true;
    }
  },
  methods: {
    submitSiteSearch: function (ev) {
      let self = this;
      let f = event.target;

      let formData = new FormData(ev.target);
      let submitUrl = f.action;
      axios
        .post(submitUrl, formData)
        .then(res => {
          console.log(res);
          let count = res.data.site_count,
            siteData = res.data.site_data;

          if (count) {
            self.$data.showResultActions = true;
            self.$data.currentPage = 1;
            self.$data.totalPages = Math.ceil(count / self.$data.pageSize);
            self.$data.searchResults = siteData.slice(0, self.$data.pageSize);
          }

        })
        .catch(err => {
          console.log(err)
        });
    },
    clearSiteSearchResults: function (ev) {
      this.$data.searchResults = [];
      this.$data.showResultActions = false;
    }
  },

});
