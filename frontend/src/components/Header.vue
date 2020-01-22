<template>
    <div class="header">
        <div class="hamburger" @click="onHamburgerClick()"><fa-icon icon="bars"/></div>
        <div class="title">{{headerInfo.title}}</div>
        <div class="subtitle">{{headerInfo.subtitle}}</div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    computed: {
        ...mapGetters(['headerInfo'])
    },
    methods: {
        onHamburgerClick: function() {
            this.$store.dispatch('openMobileSidebar');
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.header {
    height: 5rem;
    display: flex;
    align-items: center;
    padding-left: 2rem;
    background-image: linear-gradient(black, rgba(0,0,0,0));
    user-select: none;
    padding-bottom: 4px;

    .hamburger {
        margin-right: 1rem;
        margin-left: 0.25rem;
        font-size: 1.5rem;
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 4px;
        color: $primary;
        display: none;
        justify-content: center;
        align-items: center;
        cursor: pointer;

        @include breakpoint(mobile) {
            display: flex;
        }

        &:hover {
            background-color: rgb(34, 34, 34);
        }

        &:active {
            background-color: rgb(44, 44, 44);
        }
    }

    .title {
        font-size: 2rem;
        color: $primary;
        margin-right: 2rem;
    }

    .subtitle {
        font-size: 1rem;
        color: $primary;
        margin-top: 0.5rem;

        @include breakpoint(mobile) {
            display: none;
        }
    }
}
</style>
