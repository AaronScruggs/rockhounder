var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    searchResults: [
      {'site_name': 'Search to view results...'},
    ]
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
          self.$data.searchResults = res.data;

        })
        .catch(err => {
          console.log(err)
        })
      ;

    }
  }

});
