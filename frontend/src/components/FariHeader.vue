<template>
    <div class="header">
        <div class="hamburger" @click="onHamburgerClick()"><fa-icon icon="bars"/></div>
        <div class="back" v-show="displayNavigationButtons" :class="{'disabled': !backButtonAction}" @click="onBackClick()"><fa-icon icon="caret-left"/></div>
        <div class="forward disabled" v-show="displayNavigationButtons"><fa-icon icon="caret-right"/></div>
        <div class="title">{{headerInfo.title}}</div>
        <div class="subtitle">{{headerInfo.subtitle}}</div>
        <div class="spacer"></div>
        <div class="right">
            <slot name="right"></slot>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
    computed: {
        ...mapGetters(['headerInfo', 'backButtonAction', 'displayNavigationButtons']),
    },
    methods: {
        onHamburgerClick: function() {
            this.$store.dispatch('openMobileSidebar');
        },
        onBackClick: function() {
            if(!this.backButtonAction) {
                return;
            } else {
                this.backButtonAction();
            }
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
    padding-right: 2rem;
    background-image: linear-gradient(black, rgba(0,0,0,0));
    user-select: none;
    padding-bottom: 4px;

    @include breakpoint(mobile) {
        padding-left: 0.5rem;
    }

    .hamburger {
        // margin-right: 1rem;
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

    .back, .forward {
        font-size: 1.75rem;
        margin-left: 0.25rem;
        margin-right: 0.5rem;
        width: 1.75rem;
        height: 1.75rem;
        border-radius: 4px;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;

        &:hover {
            background-color: rgb(34, 34, 34);
        }

        &:active {
            background-color: rgb(44, 44, 44);
        }

        &.back {
            margin-right: 0;
            padding-right: 4px;
        }

        &.forward {
            margin-left: 0;
            padding-left: 3px;
        }

        &.disabled {
            color: #444444;
        }

        &:not(.disabled) {
            color: $primary;
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

    .spacer {
        flex-grow: 1;
    }

    .right {
        display: flex;
        align-items: center;
    }
}
</style>
