import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';

export const ProductSkeleton = () => {
  return (
    <Card className="overflow-hidden backdrop-blur-sm bg-card/50 border-border/50">
      <CardHeader className="p-0">
        <Skeleton className="h-56 w-full rounded-t-xl" />
      </CardHeader>
      <CardContent className="p-5 space-y-4">
        <Skeleton className="h-12 w-full" />
        <div className="flex items-center gap-3">
          <Skeleton className="h-7 w-24" />
          <Skeleton className="h-7 w-16" />
        </div>
        <div className="flex items-center justify-between pt-2">
          <Skeleton className="h-10 w-32" />
          <Skeleton className="h-6 w-16" />
        </div>
      </CardContent>
      <CardFooter className="p-5 pt-0">
        <Skeleton className="h-12 w-full rounded-xl" />
      </CardFooter>
    </Card>
  );
};
