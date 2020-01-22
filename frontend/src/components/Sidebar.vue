<template>
    <div class="sidebar-container" :class="{'display': displayMobileSidebar}">
        <div class="sidebar-overlay" @click="onOverlayClick()"></div>
        <div class="sidebar-content">
            <SidebarItem title="All songs" @click="onItemClick('allsongs')" :selected="selectedItem == 'allsongs'" />
            <SidebarItem title="Artists"   @click="onItemClick('artists')"  :selected="selectedItem == 'artists'"  />
            <SidebarItem title="Albums"    @click="onItemClick('albums')"   :selected="selectedItem == 'albums'"   />
            <SidebarItem title="Genres"    @click="onItemClick('genres')"   :selected="selectedItem == 'genres'"   />
            <SidebarItem title="Folders"   @click="onItemClick('folders')"  :selected="selectedItem == 'folders'"  />
            <SidebarSeparator/>
            <SidebarItem title="Queue"     @click="onItemClick('queue')"    :selected="selectedItem == 'queue'"    />
        </div>
    </div>
</template>

<script>
import SidebarItem from '@/components/SidebarItem.vue';
import SidebarSeparator from '@/components/SidebarSeparator.vue';

import { mapGetters } from 'vuex';

export default {
    components: {
        SidebarItem,
        SidebarSeparator
    },
    data: function() {
        return {
            selectedItem: '',
        };
    },
    computed: {
        ...mapGetters(['displayMobileSidebar'])
    },
    methods: {
        onItemClick: function(item) {
            if(this.selectedItem !== item) {
                this.$store.dispatch('setHeaderInfo', {});
                this.selectedItem = item;
                this.$emit('change', this.selectedItem);
                this.$store.dispatch('closeMobileSidebar');
            }

        },
        onOverlayClick: function() {
            this.$store.dispatch('closeMobileSidebar');
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

@keyframes overlay-fade {
    from {
        opacity: 0
    }

    to {
        opacity: 100;
    }
}

.sidebar-container {
    position: relative;
    z-index: 1100;

    @include breakpoint(mobile) {
        background-color: none;
        position: fixed;
        top: 0; bottom: 0; left: 0; right: 0;
        overflow: hidden;
    }

    &:not(.display) {

        @include breakpoint(mobile) {
            z-index: -1000;
        }

        .sidebar-overlay {
            @include breakpoint(mobile) {
                display: none;
            }
        }

        .sidebar-content {
            @include breakpoint(mobile) {
                transform: translateX(-100%);
            }
        }
    }

    .sidebar-overlay {
        display: none;
        position: absolute;
        top: 0; bottom: 0; left: 0; right: 0;
        background-color: rgba(0, 0, 0, 0.7);
        cursor: pointer;
        z-index: 1200;
        animation: overlay-fade 0.5s;

        @include breakpoint(mobile) {
            display: initial;
        }
    }

    .sidebar-content {
        position: absolute;
        top: 0; bottom: 0; left: 0;
        display: flex;
        flex-direction: column;
        align-items: stretch;
        padding-top: 0.5rem;
        width: 100%;
        background-color: $footer-bgcolor;
        transition: transform 0.5s;

        @include breakpoint(mobile) {
            z-index: 1300;
            width: 12rem;
            box-shadow: 3px 0px 3px rgba(0, 0, 0, 0.15);
        }
    }
}
</style>
