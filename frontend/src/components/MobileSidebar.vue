<template>
    <div class="mobile-sidebar-container">
        <Sidebar class="mobile-sidebar" :class="{'display': displayMobileSidebar}" @change="(selectedItem) => $emit('change', selectedItem)"/>
        <div class="mobile-sidebar-overlay" :class="{'display': displayMobileSidebar}" @click="onOverlayClick()"></div>
    </div>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue';

import { mapGetters } from 'vuex';

export default {
    components: {
        Sidebar
    },
    computed: {
        ...mapGetters(['displayMobileSidebar']),

    },
    methods: {
        onOverlayClick: function() {
            this.$store.dispatch('closeMobileSidebar');
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.mobile-sidebar-container {
    display: none;

    @include breakpoint(mobile) {
        display: block;
    }

    .mobile-sidebar {
        position: fixed;
        top: 0; bottom: 0; left: 0;
        transition: transform 0.4s;
        z-index: 1300;

        &:not(.display) {
            transform: translateX(-100%);
        }

        &.display {
            transform: translateX(0);
        }

    }

    .mobile-sidebar-overlay {
        z-index: 1200;
        position: fixed;
        top: 0; bottom: 0; left: 0; right: 0;
        background-color: rgba(0, 0, 0, 0.7);
        transition: opacity 0.4s;
        cursor: pointer;

        &:not(.display) {
            opacity: 0;
            pointer-events: none;
        }

        &.display {
            opacity: 1;
        }

    }

}

</style>
