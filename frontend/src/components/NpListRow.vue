<template>
    <div class="np-list-row" :class="{'cursor-pointer': $listeners.click, 'np-list-row-header': header}" v-on="$listeners">
        <div v-if="$slots.left" class="np-list-row-left" :class="{'display-hide': header}">
            <slot name="left"></slot>
        </div>
        <div class="np-list-row-grid">
            <slot></slot>
        </div>
        <div v-if="$slots.right" class="np-list-row-right" :class="{'display-hide': header}">
            <slot name="right"></slot>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        header: {
            type: Boolean,
            default: false
        }
    }
}
</script>
