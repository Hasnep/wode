function main()
infix_operators = [    "+","-","*","/"]
prefix_operators = ["-","+",""]

source=""
for _ in 1:100
    source *= rand(prefix_operators)
source *= rand('0':'9')
source *= rand(infix_operators)
end
source *= rand('0':'9')

println(source)
end
main()
