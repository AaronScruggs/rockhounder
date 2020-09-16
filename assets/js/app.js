var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    shownSearchResults: [],
    allSiteData: [],
    showResultActions: false,
    currentPage: 0,
    totalPages: 0,
    pageSize: 20
  },
  filters: {},
  computed: {
    prevResultsBtnDisabled: function (){
      return this.$data.currentPage <= 1;
    },
    nextResultsBtnDisabled: function (){
      return this.$data.currentPage >= this.$data.totalPages;
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
          let count = res.data.site_count,
            siteData = res.data.site_data;

          self.$data.allSiteData = siteData;
          self.$data.showResultActions = true;
          self.$data.currentPage = count ? 1 : 0;
          self.$data.totalPages = Math.ceil(count / self.$data.pageSize);
          self.$data.shownSearchResults = siteData.slice(0, self.$data.pageSize);

        })
        .catch(err => {
          console.log(err)
        });
    },
    clearSiteSearchResults: function (ev) {
      this.$data.shownSearchResults = [];
      this.$data.showResultActions = false;
    },
    changeResultsPage: function(ev) {
      let self = this,
        direction = ev.target.dataset.direction;

      if (direction === 'forward') {
        self.$data.currentPage += 1;
      } else if (direction === 'backward') {
        self.$data.currentPage -= 1;
      }

      let start = (self.$data.currentPage - 1) * self.$data.pageSize,
        stop = self.$data.currentPage * self.$data.pageSize;

      self.$data.shownSearchResults = self.$data.allSiteData.slice(start, stop);

    }
  },

});
