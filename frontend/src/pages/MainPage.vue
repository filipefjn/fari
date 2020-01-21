<template>
    <div class="page">
        <div class="sidebar"></div>
        <div class="content">
            <FolderNavigation/>
        </div>
        <MainPageFooter class="footer"/>
    </div>
</template>

<script>
import MainPageFooter from '@/components/MainPageFooter.vue';
import FolderNavigation from '@/components/FolderNavigation.vue';

export default {
    components: {
        MainPageFooter,
        FolderNavigation
    }
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
    }

    .footer {
        grid-row: 3 / 4;
        grid-column: 1 / 3;

        background-color: $footer-bgcolor
    }
}
</style>
