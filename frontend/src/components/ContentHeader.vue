<template>
    <div class="header">
        <div class="title">{{title}}</div>
        <div class="path">{{subtitle}}</div>
    </div>
</template>

<script>
export default {
    props: {
        title: String,
        subtitle: String
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
    background-image: linear-gradient(black, rgba(0,0,0,0));
    user-select: none;
    padding-bottom: 4px;

    .title {
        font-size: 2rem;
        color: $primary;
        margin-right: 2rem;
    }
    .path {
        font-size: 1rem;
        color: $primary;
        margin-top: 0.5rem;
    }
}
</style>
