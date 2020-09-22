var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    shownSearchResults: [],
    allSiteData: [],
    showResultActions: false,
    currentPage: 0,
    totalPages: 0,
    pageSize: 20,
    itemsPerRow: 4
  },
  filters: {},
  computed: {
    prevResultsBtnDisabled: function () {
      return this.currentPage <= 1;
    },
    nextResultsBtnDisabled: function () {
      return this.currentPage >= this.totalPages;
    },
    rowCount: function () {
      return Math.ceil(this.shownSearchResults.length / this.itemsPerRow);
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

          self.allSiteData = siteData;
          self.showResultActions = true;
          self.currentPage = count ? 1 : 0;
          self.totalPages = Math.ceil(count / self.pageSize);
          self.shownSearchResults = siteData.slice(0, self.pageSize);

        })
        .catch(err => {
          console.log(err)
        });
    },
    clearSiteSearchResults: function (ev) {
      this.shownSearchResults = [];
      this.showResultActions = false;
    },
    changeResultsPage: function (ev) {
      let self = this,
        direction = ev.target.dataset.direction;

      if (direction === 'forward') {
        self.currentPage += 1;
      } else if (direction === 'backward') {
        self.currentPage -= 1;
      }

      let start = (self.currentPage - 1) * self.pageSize,
        stop = self.currentPage * self.pageSize;

      self.shownSearchResults = self.allSiteData.slice(start, stop);
    },
    itemCountInRow: function (index) {
      return this.shownSearchResults.slice((index - 1) * this.itemsPerRow, index * this.itemsPerRow)
    }
  },

});
