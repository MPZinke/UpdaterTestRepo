# @Author: MPZinke
# @Date:   2021.11.17
# @Last Modified by:   MPZinke
# @Last Modified time: 2021.11.17


version="${1}"
message="${2}"

git commit -m "${message}"
git tag "${version}"
git push
git push origin --tags

