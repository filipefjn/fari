<template>
    <div class="np-header">
        <div class="np-header-hamburger" @click="onHamburgerClick()"><fa-icon icon="bars"/></div>
        <div class="np-header-back" @click="onBackClick()"><fa-icon icon="caret-left"/></div>
        <div class="np-header-forward" @click="onForwardClick()"><fa-icon icon="caret-right"/></div>
        <div class="np-header-title">{{headerInfo.title}}</div>
        <div class="np-header-subtitle">{{headerInfo.subtitle}}</div>
        <div class="np-header-spacer"></div>
        <div class="np-header-right">
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
            this.$router.go(-1);
        },
        onForwardClick: function() {
            this.$router.go(1);
        }
    }
}
</script>
