<template>
  <div id="app" class="w-75 mx-auto">
    <TransactionList />
  </div>
</template>

<script>
import TransactionList from './components/TransactionList.vue'

export default {
  name: 'App',
  components: {
    TransactionList
  }
}

</script>

<style>

</style>
