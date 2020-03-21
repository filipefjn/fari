<template>
    <div class="icon" :class="{'small': small}">
        <slot></slot>
    </div>
</template>

<script>
export default {
    props: {
        small: {
            type: Boolean,
            default: false
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.icon {
    margin-right: 1rem;
    font-size: 1.25rem;
    width: 1rem;
    color: $list-item-icon-color;
    display: flex;
    justify-content: center;
    align-items: center;

    &.small {
        font-size: 1rem;
    }
}
</style>
