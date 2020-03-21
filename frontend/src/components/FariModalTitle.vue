<template>
    <div class="modal-title">
        <slot></slot>
    </div>
</template>

<script>
export default {

}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.modal-title {
    margin: 1rem 0.5rem;
    margin-bottom: 0.25rem;
    font-size: 1.25rem;
}

</style>
