<template>
    <div id="app">
        <router-view name="layout">
            <transition name="content-transition" v-enter v-leave>
                <router-view name="view"/>
            </transition>
        </router-view>
    </div>
</template>

<script>
export default {

};
</script>

<style lang="scss">
@import "@/style";
</style>
