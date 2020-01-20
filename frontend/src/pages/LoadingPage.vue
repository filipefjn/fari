<template>
    <div class="page">
        <img class="loading-icon" src="@/assets/loading-white.svg"/>
    </div>
</template>

<script>
export default {

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
    display: flex;
    justify-content: center;
    align-items: center;

    .loading-icon {
        opacity: 0.06;
        height: 160px;
    }
}
</style>
