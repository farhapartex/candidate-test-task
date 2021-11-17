<template>
    <td v-if="value">{{value}}</td>
    <td v-else>-</td>
</template>

<script>
export default {
  name: 'Cell',
  props: ["value"]
}
</script>