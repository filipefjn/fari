<template>
    <div class="page">
        <MainPageSidebar class="sidebar" @change="(content) => selectedContent = content"/>
        <div class="content">
            <transition name="content-transition" v-enter v-leave>
                <FolderNavigation v-if="selectedContent == 'folders'"/>
                <Queue            v-if="selectedContent == 'queue'"  />
            </transition>
        </div>
        <MainPageFooter class="footer"/>
    </div>
</template>

<script>
import MainPageFooter from '@/components/MainPageFooter.vue';
import MainPageSidebar from '@/components/MainPageSidebar.vue';
import FolderNavigation from '@/components/FolderNavigation.vue';
import Queue from '@/components/Queue.vue';

export default {
    components: {
        MainPageFooter,
        MainPageSidebar,
        FolderNavigation,
        Queue
    },
    data: function() {
        return {
            selectedContent: '',
        };
    },
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.page {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: $page-bgcolor;
    display: grid;
    grid-template-columns: 12rem auto;
    grid-template-rows: 5rem auto 5rem;

    .sidebar {
        grid-row: 1 / 3;
        grid-column: 1 / 2;

        background-color: $sidebar-bgcolor;
    }

    .content {
        grid-row: 1 / 3;
        grid-column: 2 / 3;
        overflow-y: auto;
        position: relative;

        &> :last-child {
            padding-bottom: 2rem;
        }
    }

    .footer {
        grid-row: 3 / 4;
        grid-column: 1 / 3;

        background-color: $footer-bgcolor
    }
}

.content-transition-enter-active, .content-transition-leave-active {
    transition: opacity .3s;
    position: absolute;
    top: 0; left: 0; right: 0;
}

.content-transition-enter-active {
    z-index: 300;
}

.content-transition-leave-active {
    z-index: 200;
}

.content-transition-enter, .content-transition-leave-to {
    opacity: 0;
}
</style>
