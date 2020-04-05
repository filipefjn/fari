<template>
    <div class="sidebar-content">
        <!-- <FariSidebarItem title="All songs" @click="onItemClick('allsongs')" :selected="selectedItem == 'allsongs'" /> -->
        <FariSidebarItem title="Artists" @click="onItemClick('artists')" :selected="selectedItem == 'artists'" />
        <FariSidebarItem title="Folders" @click="onItemClick('folders')" :selected="selectedItem == 'folders'"  />
        <!-- <FariSidebarSeparator/> -->
        <FariSidebarItem title="Filter by tags" @click="onItemClick('filtertags')" :selected="selectedItem == 'filtertags'" />
        <!-- <FariSidebarSeparator/> -->
        <FariSidebarItem title="Queue" @click="onItemClick('queue')" :selected="selectedItem == 'queue'" />
        <FariSidebarSeparator/>
        <FariSidebarItem title="Server" @click="onItemClick('server')" :selected="selectedItem == 'server'" />
    </div>
</template>

<script>
import FariSidebarItem from '@/components/FariSidebarItem.vue';
import FariSidebarSeparator from '@/components/FariSidebarSeparator.vue';

import { mapGetters } from 'vuex';

export default {
    components: {
        FariSidebarItem,
        FariSidebarSeparator
    },
    data: function() {
        return {
            selectedItem: 'artists',
        };
    },
    methods: {
        onItemClick: function(item) {
            if(this.selectedItem !== item) {
                this.selectedItem = item;
                this.$store.dispatch('setHeaderInfo', {});
                this.$store.dispatch('closeMobileSidebar');
            }

        },
    },
    watch: {
        selectedItem: {
            handler: function() {
                this.$emit('change', this.selectedItem);
            },
            immediate: true
        }
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
    overflow-y: auto;

    @include breakpoint(mobile) {
        width: 12rem;
    }
}
</style>
