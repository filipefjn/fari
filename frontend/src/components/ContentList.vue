<template>
    <div class="list">
        <slot></slot>
    </div>
</template>

<script>
export default {

}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.list {
    user-select: none;
    display: flex;
    flex-direction: column;
    align-items: stretch;
}
</style>
