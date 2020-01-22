<template>
    <div class="container">
        <ContentHeader title="Queue"/>
    </div>
</template>

<script>
import ContentHeader from '@/components/ContentHeader.vue';
import ContentList from '@/components/ContentList.vue';
import ContentListItem from '@/components/ContentListItem.vue';

export default {
    components: {
        ContentHeader,
        ContentList,
        ContentListItem
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';


</style>
