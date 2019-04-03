class Solution:
    def fourSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        _len,_dict,ans = len(nums),{},set()
        nums.sort()
        if len(nums) < 4 or 4*nums[0] > target or 4*nums[_len-1] < target:
            return []
        for i in range(_len):
            for j in range(i + 1,_len):
                _sum = nums[i] + nums[j]
                if _sum not in _dict:
                    _dict[_sum] = [(i,j)]
                else:
                    _dict[_sum].append((i,j))
        for i in range(_len):
            for j in range(i + 1,_len):
                _cha = target - (nums[i] + nums[j])
                if _cha in _dict:
                    for k in _dict[_cha]:
                        if _cha == 3:
                            print [i, j, k]
                        if k[0] > j:
                            ans.add((nums[i],nums[j],nums[k[0]],nums[k[1]]))
        return list(ans)


S = Solution()
S.fourSum([-3,-2,-1,0,0,1,2,3], 0)
