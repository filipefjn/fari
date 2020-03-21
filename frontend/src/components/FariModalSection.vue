<template>
    <div class="modal-section" :class="{'no-wrap': noWrap}">
        <slot></slot>
    </div>
</template>

<script>
export default {
    props: {
        noWrap: {
            type: Boolean,
            default: false
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.modal-section {
    display: flex;
    align-items: center;
    margin: 0.5rem 0.5rem;
    padding: 0.25rem 0.5rem;
    border-radius: 6px;
    min-height: 2.5rem;
    background-color: rgb(56, 56, 56);
    box-shadow: inset 2px 2px 4px rgba(0, 0, 0, 0.15), inset -2px -2px 4px rgba(255, 255, 255, 0.03);

    &:not(.no-wrap) {
        flex-wrap: wrap;
    }
}

</style>
