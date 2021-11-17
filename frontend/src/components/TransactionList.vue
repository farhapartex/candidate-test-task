<template>
  <div class="w-100">
      <h3 class="text-center mb-5 mt-5">Transaction List</h3>
      <div class="alert alert-danger" v-if="error && status">{{error}}</div>
      <div class="alert alert-secondary" v-if="transactions.length == 0 && status==200">Sorry, No transaction found</div>
      <Table :columns="columns" :transactions="transactions" v-else />
      
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios'
import Table from "./table/Table.vue";

export default {
  name: 'TransactionList',
  components: {
    Table
  },

  data(){
      return {
          transactions: [],
          error: null,
          status: null,
          columns: ["Date", "Type", "Received Amount", "Received Currency", "Sent Amount", "Sent Currency"]
      }
  },

  mounted(){
      axios.get('http://127.0.0.1:5000/').then(response => {
          this.transactions = response.data["transactions"];
          this.status = response.status;
      }).catch(error => {
          this.error = error.response.data.error;
          this.status = error.response.status;
  })

  }
}
</script>