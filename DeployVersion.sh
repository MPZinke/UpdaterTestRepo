# @Author: MPZinke
# @Date:   2021.11.17
# @Last Modified by:   MPZinke
# @Last Modified time: 2021.11.17


version="${1}"
message="${2}"

git tag "${version}"
git commit -m "${message}"
git push --tags
git push

