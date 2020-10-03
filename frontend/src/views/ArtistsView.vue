<template>
    <div>
        <!-- TODO -->
    </div>
</template>

<script>
export default {
    beforeMount: function() {
        this.$store.dispatch('setHeaderInfo', {
            title: "Artists",
            subtitle: ""
        });
    },
    beforeDestroy: function() {
        //
    }
};
</script>
