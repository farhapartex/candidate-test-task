<template>
  <table class="table table-striped">
    <thead>
        <tr>
        <th scope="col">#</th>
        <th scope="col" v-for="(column, index) in columns" :key="index">{{column}}</th>
        
        </tr>
    </thead>
    <tbody>
        <tr v-for="(transaction, index) in transactions" :key="index">
            <th scope="row">{{index+1}}</th>
            <Cell :value="transaction.date"/>
            <Cell :value="transaction.transaction_type"/>
            <Cell :value="transaction.received_amount"/>
            <Cell :value="transaction.received_currency_iso"/>
            <Cell :value="transaction.sent_amount"/>
            <Cell :value="transaction.sent_currency_iso"/>
        </tr>
    </tbody>
   </table>
</template>

<script>
import Cell from "./Cell.vue"

export default {
  name: 'Table',
  components: {
    Cell
  },
  props: {
    transactions: Array,
    columns: Array
  }
}
</script>

