
import { VueTagsInput, createTag, createTags } from '@johmun/vue-tags-input';


var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  components: {
    VueTagsInput,
  },
  data: {
    shownSearchResults: [],
    allSearchResults: [],
    showResultActions: false,
    currentPage: 0,
    pageSize: 40,
    itemsPerRow: 4,
    tag: '',
    tags: [],
    autocompleteItems: window.commodity_choices,
  },
  filters: {},
  computed: {
    filteredItems() {
      let self = this;
      return this.autocompleteItems.filter(i => {
        // debugger;
        return i.text.toLowerCase().indexOf(this.tag.toLowerCase()) !== -1;
      });
    },
    prevResultsBtnDisabled: function () {
      return this.currentPage <= 1;
    },
    totalPages: function () {
      return Math.ceil(this.allSearchResults.length / this.pageSize);
    },
    nextResultsBtnDisabled: function () {
      return this.currentPage >= this.totalPages;
    },
    rowCount: function () {
      return Math.ceil(this.shownSearchResults.length / this.itemsPerRow);
    },
    postTags: function () {
      return this.tags.map(function(elem) {return elem.text});
    }
  },
  methods: {
    submitSiteSearch: function (ev) {
      let self = this;
      let f = event.target;

      let formData = new FormData(ev.target);
      let submitUrl = f.action;
      formData.append('tagtest', self.postTags);
      axios
        .post(submitUrl, formData)
        .then(res => {
          let count = res.data.site_count,
            siteData = res.data.site_data;

          self.allSearchResults = siteData;
          self.showResultActions = true;
          self.currentPage = count ? 1 : 0;
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

      self.shownSearchResults = self.allSearchResults.slice(start, stop);
    },
    itemCountInRow: function (index) {
      return this.shownSearchResults.slice((index - 1) * this.itemsPerRow, index * this.itemsPerRow)
    },
    updatePageSize: function (ev) {
      let pageVal = parseInt(ev.target.value);
      this.pageSize = pageVal;
      this.currentPage = 1;
      this.shownSearchResults = this.allSearchResults.slice(0, pageVal);
    }
  },

});
