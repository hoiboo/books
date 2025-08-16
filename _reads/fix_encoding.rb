#!/usr/bin/env ruby
# 检测文件名编码非 UTF-8 的文件

require 'find'
require 'pathname'

IMAGE_EXTS = %w[.jpg .jpeg .png .gif .bmp .webp .tiff].freeze

def check_filename_encoding(dir)
  Find.find(dir) do |path|
    # 排除隐藏目录（如 .git）
    if File.directory?(path) && File.basename(path).start_with?('.')
      Find.prune 
      next
    end
    
    next unless File.file?(path)
    
    next unless File.file?(path)
    
    # 过滤图片文件
    ext = File.extname(path).downcase
    next if IMAGE_EXTS.include?(ext)
    
    # 获取相对路径
    relative_path = Pathname.new(path).relative_path_from(Pathname.new(dir)).to_s
    
    # 检测文件名编码
    begin
      unless relative_path.valid_encoding? && relative_path.encoding == Encoding::UTF_8
        puts "非 UTF-8 编码文件: #{relative_path} (#{relative_path.encoding})"
      #else
      # puts "文件编码正确: #{relative_path} (#{relative_path.encoding})"
      end
    rescue ArgumentError => e
      puts "编码检测异常: #{relative_path} (#{e.message})"
    end
  end
end

if __FILE__ == $0
  require 'optparse'

  options = { directory: '.' }
  OptionParser.new do |opts|
    opts.banner = "用法: #{$0} [目录]"
    opts.on("-h", "--help", "显示帮助信息") do
      puts opts
      exit
    end
  end.parse!

  target_dir = ARGV[0] || '.' 
  abort "错误: #{target_dir} 不是有效目录" unless File.directory?(target_dir)

  puts "正在扫描目录: #{File.expand_path(target_dir)}"
  check_filename_encoding(target_dir)
end
