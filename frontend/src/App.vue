<template>
    <div>
        <MainPage/>
    </div>
</template>

<script>
import MainPage from '@/pages/MainPage.vue';

export default {
    name: 'app',
    components: {
        MainPage
    },
    created: function() {
        this.$store.dispatch('createPlayer');
    },
}
</script>

<style lang="scss">
</style>
