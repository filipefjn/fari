<template>
    <div class="context-menu-item" @click="onClick($event)">
        <slot></slot>
    </div>
</template>

<script>
export default {
    methods: {
        onClick: function(event) {
            this.$emit('click', event);
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.context-menu-item {
    font-size: 1rem;
    padding: 0.75rem 0.75rem;
    color: $text-color;
    cursor: pointer;
    white-space: nowrap;


    &:hover {
        background-color: $context-menu-hover-bgcolor;
    }
}

</style>
