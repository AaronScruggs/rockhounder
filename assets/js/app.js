var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    message: 'Hello Vue!',
    counter: 0,
    name: 'VueApp'
  },
  methods: {
    submitSiteSearch: function (ev) {
      console.log('woot');
      // let siteForm = this.$refs.siteForm;
      let f = event.target;

      let formData = new FormData(ev.target);
      let submitUrl = f.action;
      // debugger;
      axios
        .post(submitUrl, formData)
        .then(res => {
          console.log(res);
          debugger;
        })
        .catch(err => {
          console.log(err)
        })
      ;

    }
  }

});
