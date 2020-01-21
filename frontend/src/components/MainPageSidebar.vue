<template>
    <div class="sidebar">
        <SidebarItem title="All songs" @click="onItemClick('allsongs')" :selected="selectedItem == 'allsongs'" />
        <SidebarItem title="Artists"   @click="onItemClick('artists')"  :selected="selectedItem == 'artists'"  />
        <SidebarItem title="Albums"    @click="onItemClick('albums')"   :selected="selectedItem == 'albums'"   />
        <SidebarItem title="Genres"    @click="onItemClick('genres')"   :selected="selectedItem == 'genres'"   />
        <SidebarItem title="Folders"   @click="onItemClick('folders')"  :selected="selectedItem == 'folders'"  />
    </div>
</template>

<script>
import SidebarItem from '@/components/SidebarItem.vue';

export default {
    components: {
        SidebarItem
    },
    data: function() {
        return {
            selectedItem: '',
        };
    },
    methods: {
        onItemClick: function(item) {
            if(this.selectedItem !== item) {
                this.selectedItem = item;
                this.$emit('change', this.selectedItem);
            }

        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.sidebar {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    padding-top: 0.5rem;
}
</style>
