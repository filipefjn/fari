<template>
    <div class="sidebar-content">
        <SidebarItem title="All songs" @click="onItemClick('allsongs')" :selected="selectedItem == 'allsongs'" />
        <SidebarItem title="Artists"   @click="onItemClick('artists')"  :selected="selectedItem == 'artists'"  />
        <SidebarItem title="Albums"    @click="onItemClick('albums')"   :selected="selectedItem == 'albums'"   />
        <SidebarItem title="Genres"    @click="onItemClick('genres')"   :selected="selectedItem == 'genres'"   />
        <SidebarItem title="Folders"   @click="onItemClick('folders')"  :selected="selectedItem == 'folders'"  />
        <SidebarSeparator/>
        <SidebarItem title="Queue"     @click="onItemClick('queue')"    :selected="selectedItem == 'queue'"    />
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
    methods: {
        onItemClick: function(item) {
            if(this.selectedItem !== item) {
                this.$store.dispatch('setHeaderInfo', {});
                this.selectedItem = item;
                this.$emit('change', this.selectedItem);
                this.$store.dispatch('closeMobileSidebar');
            }

        },

    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.sidebar-content {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    padding-top: 0.5rem;
    width: 100%;
    background-color: $footer-bgcolor;
    overflow-y: scroll;

    @include breakpoint(mobile) {
        width: 12rem;
        box-shadow: 3px 0px 3px rgba(0, 0, 0, 0.15);
    }
}
</style>
